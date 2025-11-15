# A - Import Required Modules
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse

from .models import Customerbill
from .forms import CustomerbillForm

from customerdetailed.models import CustomerDetailed
from project.models import Project

# B - Azure Admin Check
def is_azure_admin(user):
    return user.email in [
        'admin@dzignscapeprofessionals.onmicrosoft.com',
        'based@dzignscapeprofessionals.onmicrosoft.com',
        'dulal@dzignscapeprofessionals.onmicrosoft.com',
    ]


# C - Filtering Function
def filter_customerbills(query=None, user=None, exclude_user=None):
    queryset = Customerbill.objects.all()

    if user:
        queryset = queryset.filter(created_by=user)

    if exclude_user:
        queryset = queryset.exclude(created_by=exclude_user)

    if query:
        queryset = queryset.filter(
            Q(project_name__icontains=query) |
            Q(customer_name__icontains=query)
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
def customerbill_dashboard(request):
    query = request.GET.get("q", "").strip()

    # Role-based data filtering
    if is_azure_admin(request.user):
        customerbills = filter_customerbills(query=query, exclude_user=request.user)
    else:
        customerbills = filter_customerbills(query=query, user=request.user)

    customerbills_page = get_paginated_queryset(request, customerbills)

    # ✅ Corrected form initialization
    form = CustomerbillForm(request.POST or None, user=request.user)

    # Save logic: only non-admin users can submit
    if not is_azure_admin(request.user) and request.method == "POST" and form.is_valid():
        customerbill = form.save(commit=False)
        customerbill.created_by = request.user
        customerbill.team = getattr(
            getattr(request.user, "customerbill_profile", None),
            "role",
            "sm"
        )
        customerbill.save()
        messages.success(request, "✅ Customerbill record created successfully.")
        return redirect(f"{reverse('customerbill_dashboard')}?q={query}")

    context = {
        "customerbills": customerbills_page,
        "query": query,
        "form": form,
        "mode": "list",
        "readonly": is_azure_admin(request.user)
    }
    return render(request, "customerbill/customerbill_dashboard.html", context)

# F - Admin Dashboard View (Azure Admin only, read-only)
@user_passes_test(is_azure_admin)
@login_required
def admin_dashboard(request):
    query = request.GET.get("q", "").strip()
    customerbills = filter_customerbills(query=query, exclude_user=request.user)
    customerbills_page = get_paginated_queryset(request, customerbills)

    context = {
        "customerbills": customerbills_page,
        "query": query,
        "form": CustomerbillForm(),
        "mode": "admin",
        "readonly": True
    }
    return render(request, "customerbill/customerbill_dashboard.html", context)

# G - Edit View (Only owner can edit)
@user_passes_test(lambda u: not is_azure_admin(u))
@login_required
def edit_customerbill(request, pk):
    customerbill = get_object_or_404(Customerbill, pk=pk)

    if customerbill.created_by != request.user:
        raise PermissionDenied

    query = request.GET.get("q", "").strip()
    form = CustomerbillForm(request.POST or None, instance=customerbill, user=request.user)

    if form.is_valid():
        form.save()
        messages.success(request, "✏️ Customerbill detailed record updated successfully.")
        return redirect(f"{reverse('customerbill_dashboard')}?q={query}")

    customerbills = filter_customerbills(query=query, user=request.user)
    customerbills_page = get_paginated_queryset(request, customerbills)

    context = {
        "form": form,
        "mode": "edit",
        "customerbill": customerbill,
        "query": query,
        "customerbills": customerbills_page,
        "readonly": False
    }
    return render(request, "customerbill/customerbill_dashboard.html", context)

# H - Delete View (Only owner can delete)
@user_passes_test(lambda u: not is_azure_admin(u))
@login_required
def delete_customerbill(request, pk):
    customerbill = get_object_or_404(Customerbill, pk=pk)

    if customerbill.created_by != request.user:
        raise PermissionDenied

    query = request.GET.get("q", "").strip()

    if request.method == 'POST':
        name = customerbill.project_name
        customerbill.delete()
        messages.success(request, f"🗑️ Customerbill '{name}' deleted successfully.")
        return redirect(f"{reverse('customerbill_dashboard')}?q={query}")

    return render(request, "customerbill/confirm_delete.html", {
        "customerbill": customerbill,
        "query": query
    })


