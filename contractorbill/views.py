# A - Import Required Modules
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse
from django.db.models import Q, Sum   # ✅ Added Sum here
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

# C - Filtering Function-(Project Name-Based & Contractors Company-Based)
def filter_contractorbills(query=None, user=None, exclude_user=None, project=None, contractor_company_name=None):
    queryset = Contractorbill.objects.all()

    # User-based filters
    if user:
        queryset = queryset.filter(created_by=user)

    if exclude_user:
        queryset = queryset.exclude(created_by=exclude_user)

    # Free-text search across multiple fields
    if query:
        queryset = queryset.filter(
            Q(project_name_cb__name_of_project__icontains=query) |
            Q(contractor_company_name__icontains=query)
        )

    # Step 1: Filter by Project
    if project:
        queryset = queryset.filter(project_name_cb__name_of_project__icontains=project)

        # Step 2: Filter by Contractor Company Name (only within selected project)
        if contractor_company_name:
            queryset = queryset.filter(contractor_company_name__icontains=contractor_company_name)

    else:
        # If no project is selected, allow global Contractor Company Name search
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

# E- Unified Dashboard View (Admin + Team Member)
@login_required
def contractorbill_dashboard(request):
    query = request.GET.get("q", "").strip()
    project = request.GET.get("project", "").strip() or None
    contractor_company_name = request.GET.get("contractor_company_name", "").strip() or None

    is_admin = is_azure_admin(request.user)

    # ✅ Role-based data filtering
    if is_admin:
        contractorbills = filter_contractorbills(
            query=query,
            project=project,
            contractor_company_name=contractor_company_name,
        )
    else:
        contractorbills = filter_contractorbills(
            query=query,
            user=request.user,
            project=project,
            contractor_company_name=contractor_company_name,
        )

    contractorbills_page = get_paginated_queryset(request, contractorbills)

    # ✅ Form initialization (admin + team)
    form = ContractorbillForm(request.POST or None, user=request.user)

    # ✅ Save logic: Both Admin & Team Member can submit
    if request.method == "POST" and form.is_valid():
        contractorbill = form.save(commit=False)
        contractorbill.created_by = request.user
        contractorbill.team = getattr(
            getattr(request.user, "contractorbill_profile", None),
            "role",
            "cm"
        )
        contractorbill.save()

        messages.success(request, "✅ Contractor bill record created successfully.")
        return redirect(
            f"{reverse('contractorbill_dashboard')}?q={query}&project={project or ''}&contractor_company_name={contractor_company_name or ''}"
        )

    # ✅ Calculate total bill amount for footer
    total_bill_amount = contractorbills.aggregate(Sum('bill_amount'))['bill_amount__sum'] or 0

    context = {
        "contractorbills": contractorbills_page,
        "query": query,
        "project": project or "",
        "contractor_company_name": contractor_company_name or "",
        "form": form,
        "mode": "admin" if is_admin else "list",
        "readonly": False,  # ✅ Both admin & team can save
        "total_bill_amount": total_bill_amount,
        "is_admin": is_admin,
    }

    return render(request, "contractorbill/contractorbill_dashboard.html", context)

# F - Edit View (Admin can edit all, team members only their own)
@login_required
def edit_contractorbill(request, pk):
    contractorbill = get_object_or_404(Contractorbill, pk=pk)
    is_admin = is_azure_admin(request.user)

    if not is_admin and contractorbill.created_by != request.user:
        raise PermissionDenied

    query = request.GET.get("q", "").strip()
    project = request.GET.get("project", "").strip() or ""
    contractor_company_name = request.GET.get("contractor_company_name", "").strip() or ""

    form = ContractorbillForm(request.POST or None, instance=contractorbill, user=request.user)

    if form.is_valid():
        form.save()
        messages.success(request, "✏️ Contractor bill updated successfully.")
        return redirect(
            f"{reverse('contractorbill_dashboard')}?q={query}&project={project}&contractor_company_name={contractor_company_name}"
        )
    contractorbills = filter_contractorbills(
        query=query,
        exclude_user=request.user if is_admin else None,
        user=None if is_admin else request.user,
        project=project or None,
        contractor_company_name=contractor_company_name or None,
    )
    contractorbills_page = get_paginated_queryset(request, contractorbills)

    total_bill_amount = contractorbills.aggregate(Sum('bill_amount'))['bill_amount__sum'] or 0

    context = {
        "form": form,
        "mode": "edit",
        "contractorbill": contractorbill,
        "query": query,
        "project": project,
        "contractor_company_name": contractor_company_name,
        "contractorbills": contractorbills_page,
        "readonly": False,
        "is_admin": is_admin,
        "total_bill_amount": total_bill_amount,
    }

    return render(request, "contractorbill/contractorbill_dashboard.html", context)

# G - Delete View (Admin can delete all, team members only their own)
@login_required
def delete_contractorbill(request, pk):
    contractorbill = get_object_or_404(Contractorbill, pk=pk)
    is_admin = is_azure_admin(request.user)

    if not is_admin and contractorbill.created_by != request.user:
        raise PermissionDenied

    contractorbill.delete()
    messages.success(request, "🗑️ Contractor bill deleted successfully.")

    query = request.GET.get("q", "").strip()
    project = request.GET.get("project", "").strip() or ""
    contractor_company_name = request.GET.get("contractor_company_name", "").strip() or ""

    return redirect(
        f"{reverse('contractorbill_dashboard')}?q={query}&project={project}&contractor_company_name={contractor_company_name}"
    )

# H - Auto-Fill-API View-(used by JavaScript)
def get_contractorbill_details(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return JsonResponse({
        "project_address": project.project_address or "",   # ✅ safe return
    })
