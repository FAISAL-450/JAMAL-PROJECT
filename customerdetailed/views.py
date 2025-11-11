# A - Import Required Modules
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied

from .models import CustomerDetailed
from .forms import CustomerDetailedForm

# B - Azure Admin Check
def is_azure_admin(user):
    return user.email == 'admin@dzignscapeprofessionals.onmicrosoft.com'

# C - Filtering Function
def filter_customerdetaileds(query=None, user=None, exclude_user=None):
    queryset = CustomerDetailed.objects.all()

    if user:
        queryset = queryset.filter(created_by=user)

    if exclude_user:
        queryset = queryset.exclude(created_by=exclude_user)

    if query:
        queryset = queryset.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(company__icontains=query)
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
def customerdetailed_dashboard(request):
    query = request.GET.get("q", "").strip()
    form = CustomerDetailedForm(request.POST or None)

    # Role-based data filtering
    if is_azure_admin(request.user):
        customerdetaileds = filter_customerdetaileds(query=query, exclude_user=request.user)
    else:
        customerdetaileds = filter_customerdetaileds(query=query, user=request.user)

    customerdetaileds_page = get_paginated_queryset(request, customerdetaileds)

    # Save logic: only non-admin users can submit
    if not is_azure_admin(request.user) and request.method == "POST" and form.is_valid():
        customer = form.save(commit=False)
        customer.created_by = request.user
        customer.team = getattr(
            getattr(request.user, "customerdetailed_profile", None),
            "role",
            "support"
        )
        customer.save()
        messages.success(request, "✅ Customer detailed record created successfully.")
        return redirect(f"{reverse('customerdetailed_dashboard')}?q={query}")

    context = {
        "customerdetaileds": customerdetaileds_page,
        "query": query,
        "form": form,
        "mode": "list",
        "readonly": is_azure_admin(request.user)
    }
    return render(request, "customerdetailed/customerdetailed_dashboard.html", context)

# F - Admin Dashboard View (Azure Admin only, read-only)
@user_passes_test(is_azure_admin)
@login_required
def admin_dashboard(request):
    query = request.GET.get("q", "").strip()
    customerdetaileds = filter_customerdetaileds(query=query, exclude_user=request.user)
    customerdetaileds_page = get_paginated_queryset(request, customerdetaileds)

    context = {
        "customerdetaileds": customerdetaileds_page,
        "query": query,
        "form": CustomerDetailedForm(),
        "mode": "admin",
        "readonly": True
    }
    return render(request, "customerdetailed/customerdetailed_dashboard.html", context)

# G - Edit View (Only owner can edit)
@user_passes_test(lambda u: not is_azure_admin(u))
@login_required
def edit_customer(request, pk):
    customer = get_object_or_404(CustomerDetailed, pk=pk)

    if customer.created_by != request.user:
        raise PermissionDenied

    query = request.GET.get("q", "").strip()
    form = CustomerDetailedForm(request.POST or None, instance=customer)

    if form.is_valid():
        form.save()
        messages.success(request, "✏️ Customer detailed record updated successfully.")
        return redirect(f"{reverse('customerdetailed_dashboard')}?q={query}")

    customerdetaileds = filter_customerdetaileds(query=query, user=request.user)
    customerdetaileds_page = get_paginated_queryset(request, customerdetaileds)

    context = {
        "form": form,
        "mode": "edit",
        "customer": customer,
        "query": query,
        "customerdetaileds": customerdetaileds_page,
        "readonly": False
    }
    return render(request, "customerdetailed/customerdetailed_dashboard.html", context)

# H - Delete View (Only owner can delete)
@user_passes_test(lambda u: not is_azure_admin(u))
@login_required
def delete_customer(request, pk):
    customer = get_object_or_404(CustomerDetailed, pk=pk)

    if customer.created_by != request.user:
        raise PermissionDenied

    query = request.GET.get("q", "").strip()

    if request.method == 'POST':
        name = customer.name
        customer.delete()
        messages.success(request, f"🗑️ Customer '{name}' deleted successfully.")
        return redirect(f"{reverse('customerdetailed_dashboard')}?q={query}")

    return render(request, "customerdetailed/confirm_delete.html", {
        "customer": customer,
        "query": query
    })
