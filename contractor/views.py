# A - Import Required Modules
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied

from .models import Contractor
from .forms import ContractorForm

# B - Azure Admin Check
def is_azure_admin(user):
    return user.email == 'admin@dzignscapeprofessionals.onmicrosoft.com'

# C - Filtering Function
def filter_contractors(query=None, user=None, exclude_user=None):
    queryset = Contractor.objects.all()

    if user:
        queryset = queryset.filter(created_by=user)

    if exclude_user:
        queryset = queryset.exclude(created_by=exclude_user)

    if query:
        queryset = queryset.filter(
            Q(contractor_company__icontains=query) |
            Q(name_of_contractor__icontains=query) |
            Q(contractor_phone_number__icontains=query)
        )

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

# E - Team Dashboard View (List View + Form Submission)
@login_required
def contractor_dashboard(request):
    query = request.GET.get("q", "").strip()
    form = ContractorForm(request.POST or None)

    # Role-based data filtering
    if is_azure_admin(request.user):
        contractors = filter_contractors(query=query, exclude_user=request.user)
    else:
        contractors = filter_contractors(query=query, user=request.user)

    contractors_page = get_paginated_queryset(request, contractors)

    # Save logic: only non-admin users can submit
    if not is_azure_admin(request.user) and request.method == "POST" and form.is_valid():
        contractor = form.save(commit=False)
        contractor.created_by = request.user
        contractor.team = getattr(
            getattr(request.user, "contractor_profile", None),
            "role",
            "planner"
        )
        contractor.save()
        messages.success(request, "✅ Contractor detailed record created successfully.")
        return redirect(f"{reverse('contractor_dashboard')}?q={query}")

    context = {
        "contractors": contractors_page,
        "query": query,
        "form": form,
        "mode": "list",
        "readonly": is_azure_admin(request.user)
    }
    return render(request, "contractor/contractor_dashboard.html", context)

# F - Admin Dashboard View (Azure Admin only, read-only)
@login_required
@user_passes_test(is_azure_admin)
def admin_dashboard(request):
    query = request.GET.get("q", "").strip()
    contractors = filter_contractors(query=query, exclude_user=request.user)
    contractors_page = get_paginated_queryset(request, contractors)

    context = {
        "contractors": contractors_page,
        "query": query,
        "form": ContractorForm(),
        "mode": "admin",
        "readonly": True
    }
    return render(request, "contractor/contractor_dashboard.html", context)

# G - Edit View (Only owner can edit)
@login_required
@user_passes_test(lambda u: not is_azure_admin(u))
def edit_contractor(request, pk):
    contractor = get_object_or_404(Contractor, pk=pk)

    if contractor.created_by != request.user:
        raise PermissionDenied

    query = request.GET.get("q", "").strip()
    form = ContractorForm(request.POST or None, instance=contractor)

    if form.is_valid():
        form.save()
        messages.success(request, "✏️ Contractor detailed record updated successfully.")
        return redirect(f"{reverse('contractor_dashboard')}?q={query}")

    contractors = filter_contractors(query=query, user=request.user)
    contractors_page = get_paginated_queryset(request, contractors)

    context = {
        "form": form,
        "mode": "edit",
        "contractor": contractor,
        "query": query,
        "contractors": contractors_page,
        "readonly": False
    }
    return render(request, "contractor/contractor_dashboard.html", context)

# H - Delete View (Only owner can delete)
@login_required
@user_passes_test(lambda u: not is_azure_admin(u))
def delete_contractor(request, pk):
    contractor = get_object_or_404(Contractor, pk=pk)

    if contractor.created_by != request.user:
        raise PermissionDenied

    query = request.GET.get("q", "").strip()

    if request.method == 'POST':
        name = contractor.contractor_company
        contractor.delete()
        messages.success(request, f"🗑️ Contractor '{name}' deleted successfully.")
        return redirect(f"{reverse('contractor_dashboard')}?q={query}")

    return render(request, "contractor/confirm_delete.html", {
        "contractor": contractor,
        "query": query
    })

