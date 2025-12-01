# A - Import Required Modules
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied

from .models import RequisitionItem
from .forms import RequisitionItemForm

# B - Azure Admin Check
def is_azure_admin(user):
    return user.email == 'admin@dzignscapeprofessionals.onmicrosoft.com'

# C - Filtering Function
def filter_requisitions(query=None, user=None, exclude_user=None, project=None, pr_no=None):
    queryset = RequisitionItem.objects.all()

    # User-based filters
    if user:
        queryset = queryset.filter(created_by=user)

    if exclude_user:
        queryset = queryset.exclude(created_by=exclude_user)

    # Free-text search across multiple fields
    if query:
        queryset = queryset.filter(
            Q(PR_no__icontains=query) |
            Q(name_of_resource__icontains=query) |
            Q(project_name_fpr__name_of_project__icontains=query)
        )

    # Step 1: Filter by Project
    if project:
        queryset = queryset.filter(project_name_fpr__name_of_project__icontains=project)

        # Step 2: Filter by PR No (only within selected project)
        if pr_no:
            queryset = queryset.filter(PR_no__icontains=pr_no)

    else:
        # If no project is selected, allow global PR No search
        if pr_no:
            queryset = queryset.filter(PR_no__icontains=pr_no)

    return queryset

# D - Reusable Pagination Function
def get_paginated_queryset(request, queryset, per_page=10):
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get("page")

    try:
        return paginator.page(page_number)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)

# E - Team Dashboard View
@login_required
def requisition_dashboard(request):
    query = request.GET.get("q", "").strip()
    project = request.GET.get("project", "").strip()
    pr_no = request.GET.get("pr_no", "").strip()

    form = RequisitionItemForm(request.POST or None, user=request.user)
    is_admin = is_azure_admin(request.user)

    requisitions = filter_requisitions(
        query=query,
        user=request.user if not is_admin else None,
        project=project,
        pr_no=pr_no
    )
    requisitions_page = get_paginated_queryset(request, requisitions)

    if not is_admin and request.method == "POST" and form.is_valid():
        requisition = form.save(commit=False)
        requisition.created_by = request.user
        requisition.updated_by = request.user
        profile = getattr(request.user, "requisition_profile", None)
        requisition.team = getattr(profile, "role", "pr-manager")
        requisition.save()
        messages.success(request, "✅ Requisition record created successfully.")
        return redirect(
            f"{reverse('requisition_dashboard')}?q={query}&project={project}&pr_no={pr_no}"
        )

    context = {
        "requisitions": requisitions_page,
        "query": query,
        "project": project,
        "pr_no": pr_no,
        "form": form,
        "mode": "list",
        "readonly": is_admin,
        "is_admin": is_admin,
        "current_user": request.user,
    }
    return render(request, "requisition/requisition_dashboard.html", context)

# F - Admin Dashboard View
@user_passes_test(is_azure_admin)
@login_required
def admin_dashboard(request):
    query = request.GET.get("q", "").strip()
    project = request.GET.get("project", "").strip()
    pr_no = request.GET.get("pr_no", "").strip()

    requisitions = filter_requisitions(
        query=query,
        project=project,
        pr_no=pr_no
    )
    requisitions_page = get_paginated_queryset(request, requisitions)

    context = {
        "requisitions": requisitions_page,
        "query": query,
        "project": project,
        "pr_no": pr_no,
        "form": RequisitionItemForm(user=request.user),
        "mode": "admin",
        "readonly": True,
        "is_admin": True,
        "current_user": request.user,
    }
    return render(request, "requisition/requisition_dashboard.html", context)

# G - Edit View
@login_required
def edit_requisition(request, pk):
    requisition = get_object_or_404(RequisitionItem, pk=pk)
    is_admin = is_azure_admin(request.user)

    if not (is_admin or (requisition.created_by == request.user and requisition.allow_team_edit)):
        raise PermissionDenied

    query = request.GET.get("q", "").strip()
    form = RequisitionItemForm(request.POST or None, instance=requisition, user=request.user)

    if form.is_valid():
        updated_req = form.save(commit=False)
        updated_req.updated_by = request.user

        # Reset team permission after edit
        if not is_admin:
            updated_req.allow_team_edit = False
            updated_req.edit_request_pending = False

        updated_req.save()
        messages.success(request, "✏️ Requisition record updated successfully.")
        redirect_url = 'admin_dashboard' if is_admin else 'requisition_dashboard'
        return redirect(f"{reverse(redirect_url)}?q={query}")

    requisitions = filter_requisitions(query=query, user=request.user if not is_admin else None)
    requisitions_page = get_paginated_queryset(request, requisitions)

    context = {
        "form": form,
        "mode": "edit",
        "requisition": requisition,
        "query": query,
        "requisitions": requisitions_page,
        "readonly": is_admin,
        "is_admin": is_admin,
        "current_user": request.user,
    }
    return render(request, "requisition/requisition_dashboard.html", context)

# H - Delete View
@login_required
def delete_requisition(request, pk):
    requisition = get_object_or_404(RequisitionItem, pk=pk)
    is_admin = is_azure_admin(request.user)

    if not (is_admin or (requisition.created_by == request.user and requisition.allow_team_edit)):
        raise PermissionDenied

    query = request.GET.get("q", "").strip()

    if request.method == 'POST':
        pr_no = requisition.PR_no
        requisition.delete()
        messages.success(request, f"🗑️ Requisition '{pr_no}' deleted successfully.")
        redirect_url = 'admin_dashboard' if is_admin else 'requisition_dashboard'
        return redirect(f"{reverse(redirect_url)}?q={query}")

    return render(request, "requisition/confirm_delete.html", {
        "requisition": requisition,
        "query": query,
    })

# I - Admin Approves Edit/Delete Request
@user_passes_test(is_azure_admin)
@login_required
def approve_team_permission(request, pk):
    requisition = get_object_or_404(RequisitionItem, pk=pk)
    requisition.allow_team_edit = True
    requisition.edit_request_pending = False
    requisition.updated_by = request.user
    requisition.save()
    messages.success(request, f"✅ Edit/delete permission granted for '{requisition.PR_no}'. Team member can now proceed.")
    return redirect(reverse('admin_dashboard'))

# J - Team Member Requests Edit/Delete Access
@login_required
def request_team_permission(request, pk):
    requisition = get_object_or_404(RequisitionItem, pk=pk)

    if requisition.created_by != request.user:
        raise PermissionDenied

    if not requisition.edit_request_pending:
        requisition.edit_request_pending = True
        requisition.save()
        messages.success(request, f"📩 Request sent to admin for '{requisition.PR_no}'. Awaiting approval.")
    else:
        messages.info(request, f"⏳ Request already pending for '{requisition.PR_no}'.")

    return redirect(reverse('requisition_dashboard'))
