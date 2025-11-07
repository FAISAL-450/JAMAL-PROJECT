# A - Import Required Modules
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .models import CustomerDetailed
from .forms import CustomerDetailedForm

# B - Azure Admin Check
def is_azure_admin(user):
    return user.email.lower() == 'admin@dzignscapeprofessionals.onmicrosoft.com'

# C - Filtering Function
def filter_customerdetaileds(query=None, user=None, admin_view=False):
    queryset = CustomerDetailed.objects.all()

    if not admin_view and user:
        queryset = queryset.filter(created_by=user)

    if query:
        queryset = queryset.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(company__icontains=query)
        )

    return queryset.order_by('-id')

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

# E - Team Member Dashboard View
@login_required
def customerdetailed_dashboard(request):
    query = request.GET.get("q", "").strip()
    is_admin = is_azure_admin(request.user)

    customerdetaileds = filter_customerdetaileds(query=query, user=request.user, admin_view=is_admin)
    customerdetaileds_page = get_paginated_queryset(request, customerdetaileds)

    form = CustomerDetailedForm(request.POST or None) if not is_admin else None

    if not is_admin and request.method == "POST" and form.is_valid():
        customer = form.save(commit=False)
        customer.created_by = request.user
        customer.team = getattr(request.user.customerdetailed_profile, "role", None)
        customer.save()
        messages.success(request, "✅ Customer detailed record created successfully.")
        return redirect(f"{reverse('customerdetailed_dashboard')}?q={query}")

    return render(request, "customerdetailed/customerdetailed_dashboard.html", {
        "customerdetaileds": customerdetaileds_page,
        "query": query,
        "form": form,
        "mode": "list",
        "readonly": is_admin
    })

# F - Admin Dashboard View (Read-only)
@login_required
def admin_dashboard(request):
    if not is_azure_admin(request.user):
        raise PermissionDenied

    query = request.GET.get("q", "").strip()
    customerdetaileds = filter_customerdetaileds(query=query, admin_view=True)
    customerdetaileds_page = get_paginated_queryset(request, customerdetaileds)

    return render(request, "customerdetailed/customerdetailed_dashboard.html", {
        "customerdetaileds": customerdetaileds_page,
        "query": query,
        "form": None,
        "mode": "admin",
        "readonly": True
    })

# G - Edit View (Only team member can edit their own)
@login_required
def edit_customer(request, pk):
    customer = get_object_or_404(CustomerDetailed, pk=pk)

    if is_azure_admin(request.user) or customer.created_by != request.user:
        raise PermissionDenied

    query = request.GET.get("q", "").strip()
    form = CustomerDetailedForm(request.POST or None, instance=customer)

    if form.is_valid():
        form.save()
        messages.success(request, "✏️ Customer detailed record updated successfully.")
        return redirect(f"{reverse('customerdetailed_dashboard')}?q={query}")

    customerdetaileds = filter_customerdetaileds(query=query, user=request.user)
    customerdetaileds_page = get_paginated_queryset(request, customerdetaileds)

    return render(request, "customerdetailed/customerdetailed_dashboard.html", {
        "form": form,
        "mode": "edit",
        "customer": customer,
        "query": query,
        "customerdetaileds": customerdetaileds_page,
        "readonly": False
    })

# H - Delete View (Only team member can delete their own)
@login_required
def delete_customer(request, pk):
    customer = get_object_or_404(CustomerDetailed, pk=pk)

    if is_azure_admin(request.user) or customer.created_by != request.user:
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

