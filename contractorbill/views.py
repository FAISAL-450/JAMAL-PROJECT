# A - Import Required Modules
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse
from django.db.models import Q, Sum
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse

from .models import Contractorbill
from .forms import ContractorbillForm
from project.models import Project

# B - Azure Admin Check
def is_azure_admin(user):
    return user.email == 'admin@dzignscapeprofessionals.onmicrosoft.com'

# C - Filtering Function (Project Name-Based & Contractor Company-Based)
def filter_contractorbills(query=None, user=None, exclude_user=None, project=None, contractor_company_name=None):
    queryset = Contractorbill.objects.all()

    # User-based filters
    if user:
        queryset = queryset.filter(created_by=user)

    if exclude_user:
        queryset = queryset.exclude(created_by=exclude_user)

    # Free-text search
    if query:
        queryset = queryset.filter(
            Q(project_name_cb__name_of_project__icontains=query) |
            Q(contractor_company_name__icontains=query)
        )

    # Project filter
    if project:
        queryset = queryset.filter(project_name_cb__name_of_project__icontains=project)

        # Contractor company filter within project
        if contractor_company_name:
            queryset = queryset.filter(contractor_company_name__icontains=contractor_company_name)

    else:
        # Global contractor company search
        if contractor_company_name:
            queryset = queryset.filter(contractor_company_name__icontains=contractor_company_name)

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
def contractorbill_dashboard(request):
    query = request.GET.get("q", "").strip()
    project = request.GET.get("project", "").strip() or None
    contractor_company_name = request.GET.get("contractor_company_name", "").strip() or None

    is_admin = is_azure_admin(request.user)

    # ✅ Team member sees only their own records
    contractorbills = filter_contractorbills(
        query=query,
        user=request.user,
        project=project,
        contractor_company_name=contractor_company_name,
    )

    contractorbills_page = get_paginated_queryset(request, contractorbills)

    # ✅ Form initialization
    form = ContractorbillForm(request.POST or None, user=request.user)

    # ✅ Team member can add new records
    if not is_admin and request.method == "POST" and form.is_valid():
        contractorbill = form.save(commit=False)
        contractorbill.created_by = request.user
        profile = getattr(request.user, "contractorbill_profile", None)
        contractorbill.team = getattr(profile, "role", "cm")
        contractorbill.save()
        messages.success(request, "✅ Contractor bill created successfully.")
        return redirect(f"{reverse('contractorbill_dashboard')}?q={query}")

    # ✅ Total amount
    total_bill_amount = contractorbills.aggregate(Sum('bill_amount'))['bill_amount__sum'] or 0

    context = {
        "contractorbills": contractorbills_page,
        "query": query,
        "project": project or "",
        "contractor_company_name": contractor_company_name or "",
        "form": form,
        "mode": "list",
        "readonly": is_admin,
        "is_admin": is_admin,
        "total_bill_amount": total_bill_amount,
        "current_user": request.user,
    }
    return render(request, "contractorbill/contractorbill_dashboard.html", context)

# F - Admin Dashboard View
@user_passes_test(is_azure_admin)
@login_required
def contractorbill_admin_dashboard(request):
    query = request.GET.get("q", "").strip()
    project = request.GET.get("project", "").strip() or None
    contractor_company_name = request.GET.get("contractor_company_name", "").strip() or None

    # ✅ Admin sees ALL records
    contractorbills = filter_contractorbills(
        query=query,
        project=project,
        contractor_company_name=contractor_company_name,
    )

    contractorbills_page = get_paginated_queryset(request, contractorbills)

    total_bill_amount = contractorbills.aggregate(Sum('bill_amount'))['bill_amount__sum'] or 0

    context = {
        "contractorbills": contractorbills_page,
        "query": query,
        "project": project or "",
        "contractor_company_name": contractor_company_name or "",
        "form": ContractorbillForm(),
        "mode": "admin",
        "readonly": True,
        "is_admin": True,
        "total_bill_amount": total_bill_amount,
        "current_user": request.user,
    }
    return render(request, "contractorbill/contractorbill_dashboard.html", context)

# G - Edit View
@login_required
def contractorbill_edit_contractorbill(request, pk):
    contractorbill = get_object_or_404(Contractorbill, pk=pk)

    # ✅ Only the owner can edit
    if contractorbill.created_by != request.user:
        raise PermissionDenied

    query = request.GET.get("q", "").strip()
    form = ContractorbillForm(request.POST or None, instance=contractorbill)

    if form.is_valid():
        updated_contractorbill = form.save(commit=False)
        updated_contractorbill.updated_by = request.user
        updated_contractorbill.save()

        messages.success(request, "✏️ Contractor bill updated successfully.")
        return redirect(f"{reverse('contractorbill_dashboard')}?q={query}")

    contractorbills = filter_contractorbills(query=query, user=request.user)
    contractorbills_page = get_paginated_queryset(request, contractorbills)

    context = {
        "form": form,
        "mode": "edit",
        "contractorbill": contractorbill,
        "query": query,
        "contractorbills": contractorbills_page,
        "readonly": False,  # ✅ Owner can edit
        "is_admin": False,  # ✅ Admin cannot edit
        "current_user": request.user,
    }
    return render(request, "contractorbill/contractorbill_dashboard.html", context)

# H - Delete View
@login_required
def contractorbill_delete_contractorbill(request, pk):
    contractorbill = get_object_or_404(Contractorbill, pk=pk)

    # ✅ Only the owner can delete
    if contractorbill.created_by != request.user:
        raise PermissionDenied

    query = request.GET.get("q", "").strip()

    if request.method == "POST":
        name = contractorbill.contractor_company_name
        contractorbill.delete()

        messages.success(request, f"🗑️ Contractor bill '{name}' deleted successfully.")
        return redirect(f"{reverse('contractorbill_dashboard')}?q={query}")

    return render(request, "contractorbill/confirm_delete.html", {
        "contractorbill": contractorbill,
        "query": query
    })

# I - Admin Approves Edit/Delete Request
@user_passes_test(is_azure_admin)
@login_required
def contractorbill_approve_team_permission(request, pk):
    contractorbill = get_object_or_404(Contractorbill, pk=pk)
    contractorbill.allow_team_edit = True
    contractorbill.edit_request_pending = False
    contractorbill.updated_by = request.user
    contractorbill.save()

    messages.success(
        request,
        f"✅ Edit/delete permission granted for '{contractorbill.contractor_company_name}'."
    )
    return redirect(reverse('contractorbill_admin_dashboard'))

# J - Team Member Requests Edit/Delete Access
@login_required
def contractorbill_request_team_permission(request, pk):
    contractorbill = get_object_or_404(Contractorbill, pk=pk)

    if contractorbill.created_by != request.user:
        raise PermissionDenied

    if not contractorbill.edit_request_pending:
        contractorbill.edit_request_pending = True
        contractorbill.save()
        messages.success(
            request,
            f"📩 Request sent to admin for '{contractorbill.contractor_company_name}'. Awaiting approval."
        )
    else:
        messages.info(
            request,
            f"⏳ Request already pending for '{contractorbill.contractor_company_name}'."
        )

    return redirect(reverse('contractorbill_dashboard'))

# K - Auto-Fill API (Used by JavaScript)
def get_contractorbill_details(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return JsonResponse({
        "project_address": project.project_address or "",
    })
