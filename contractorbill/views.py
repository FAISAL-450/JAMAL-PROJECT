# A - Import Required Modules
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse
from django.db.models import Q
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

# C - Filtering Function
def filter_contractorbills(query=None, user=None, exclude_user=None):
    queryset = Contractorbill.objects.all()

    if user:
        queryset = queryset.filter(created_by=user)

    if exclude_user:
        queryset = queryset.exclude(created_by=exclude_user)

    if query:
        queryset = queryset.filter(
            Q(project_name_cb__name_of_project__icontains=query) |
            Q(contractor_company_name__icontains=query) |
            Q(name_of_work__icontains=query)
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
def contractorbill_dashboard(request):
    query = request.GET.get("q", "").strip()
    form = ContractorbillForm(request.POST or None)

    # Role-based data filtering
    if is_azure_admin(request.user):
        contractorbills = filter_contractorbills(query=query, exclude_user=request.user)
    else:
        contractorbills = filter_contractorbills(query=query, user=request.user)

    contractorbills_page = get_paginated_queryset(request, contractorbills)

    # Save logic: Team member can submit
    if not is_azure_admin(request.user) and request.method == "POST" and form.is_valid():
        contractorbill = form.save(commit=False)
        contractorbill.created_by = request.user
        contractorbill.team = getattr(
            getattr(request.user, "contractorbill_profile", None),
            "role",
            "cm"   # ✅ default role for contractor bills
        )
        contractorbill.save()
        messages.success(request, "✅ Contractorbill detailed record created successfully.")
        return redirect(f"{reverse('contractorbill_dashboard')}?q={query}")

    context = {
        "contractorbills": contractorbills_page,
        "query": query,
        "form": form,
        "mode": "list",
        "readonly": is_azure_admin(request.user)
    }
    return render(request, "contractorbill/contractorbill_dashboard.html", context)

# F - Admin Dashboard View (Azure Admin only, read-only)
@user_passes_test(is_azure_admin)
@login_required
def admin_dashboard(request):
    query = request.GET.get("q", "").strip()
    contractorbills = filter_contractorbills(query=query, exclude_user=request.user)
    contractorbills_page = get_paginated_queryset(request, contractorbills)

    context = {
        "contractorbills": contractorbills_page,
        "query": query,
        "form": ContractorbillForm(),
        "mode": "admin",
        "readonly": True
    }
    return render(request, "contractorbill/contractorbill_dashboard.html", context)

# G - Edit View (Team member can edit)
@user_passes_test(lambda u: not is_azure_admin(u))
@login_required
def edit_contractorbill(request, pk):
    contractorbill = get_object_or_404(Contractorbill, pk=pk)

    if contractorbill.created_by != request.user:
        raise PermissionDenied

    query = request.GET.get("q", "").strip()
    form = ContractorbillForm(request.POST or None, instance=contractorbill)

    if form.is_valid():
        form.save()
        messages.success(request, "✏️ Contractorbill detailed record updated successfully.")
        return redirect(f"{reverse('contractorbill_dashboard')}?q={query}")

    contractorbills = filter_contractorbills(query=query, user=request.user)
    contractorbills_page = get_paginated_queryset(request, contractorbills)

    context = {
        "form": form,
        "mode": "edit",
        "contractorbill": contractorbill,
        "query": query,
        "contractorbills": contractorbills_page,
        "readonly": False
    }
    return render(request, "contractorbill/contractorbill_dashboard.html", context)

# H - Delete View (Team member can delete)
@user_passes_test(lambda u: not is_azure_admin(u))
@login_required
def delete_contractorbill(request, pk):
    contractorbill = get_object_or_404(Contractorbill, pk=pk)

    if contractorbill.created_by != request.user:
        raise PermissionDenied

    query = request.GET.get("q", "").strip()

    if request.method == 'POST':
        name = contractorbill.contractor_company_name
        contractorbill.delete()
        messages.success(request, f"🗑️ Contractorbill '{name}' deleted successfully.")
        return redirect(f"{reverse('contractorbill_dashboard')}?q={query}")

    return render(request, "contractorbill/confirm_delete.html", {
        "contractorbill": contractorbill,
        "query": query
    })

# I - Auto-Fill API View (used by JavaScript)
def get_contractorbill_details(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return JsonResponse({
        "project_address": project.project_address or "",   # ✅ safe return
    })

