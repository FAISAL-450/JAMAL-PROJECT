# A - Import Required Modules
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied

from .models import Supplier
from .forms import SupplierForm

# B - Azure Admin Check
def is_azure_admin(user):
    return user.email == 'admin@dzignscapeprofessionals.onmicrosoft.com'

# C - Filtering Function
def filter_suppliers(query=None, user=None, exclude_user=None):
    queryset = Supplier.objects.all()

    if user:
        queryset = queryset.filter(created_by=user)

    if exclude_user:
        queryset = queryset.exclude(created_by=exclude_user)

    if query:
        queryset = queryset.filter(
            Q(name_of_supplier__icontains=query) |
            Q(supplier_address__icontains=query) |
            Q(supplier_contact_person__icontains=query)
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
def supplier_dashboard(request):
    query = request.GET.get("q", "").strip()
    form = SupplierForm(request.POST or None)

    # Role-based data filtering
    if is_azure_admin(request.user):
        suppliers = filter_suppliers(query=query, exclude_user=request.user)
    else:
        suppliers = filter_suppliers(query=query, user=request.user)

    suppliers_page = get_paginated_queryset(request, suppliers)

    # Save logic: Team member can submit
    if not is_azure_admin(request.user) and request.method == "POST" and form.is_valid():
        supplier = form.save(commit=False)
        supplier.created_by = request.user
        supplier.team = getattr(
            getattr(request.user, "supplier_profile", None),
            "role",
            "pm"
        )
        supplier.save()
        messages.success(request, "✅ Supplier detailed record created successfully.")
        return redirect(f"{reverse('supplier_dashboard')}?q={query}")

    context = {
        "suppliers": suppliers_page,
        "query": query,
        "form": form,
        "mode": "list",
        "readonly": is_azure_admin(request.user)
    }
    return render(request, "supplier/supplier_dashboard.html", context)

# F - Admin Dashboard View (Azure Admin only, read-only)
@user_passes_test(is_azure_admin)
@login_required
def admin_dashboard(request):
    query = request.GET.get("q", "").strip()
    suppliers = filter_suppliers(query=query, exclude_user=request.user)
    suppliers_page = get_paginated_queryset(request, suppliers)

    context = {
        "suppliers": suppliers_page,
        "query": query,
        "form": SupplierForm(),
        "mode": "admin",
        "readonly": True
    }
    return render(request, "supplier/supplier_dashboard.html", context)

# G - Edit View (Team member can edit)
@user_passes_test(lambda u: not is_azure_admin(u))
@login_required
def edit_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)

    if supplier.created_by != request.user:
        raise PermissionDenied

    query = request.GET.get("q", "").strip()
    form = SupplierForm(request.POST or None, instance=supplier)

    if form.is_valid():
        form.save()
        messages.success(request, "✏️ Supplier detailed record updated successfully.")
        return redirect(f"{reverse('supplier_dashboard')}?q={query}")

    suppliers = filter_suppliers(query=query, user=request.user)
    suppliers_page = get_paginated_queryset(request, suppliers)

    context = {
        "form": form,
        "mode": "edit",
        "supplier": supplier,
        "query": query,
        "suppliers": suppliers_page,
        "readonly": False
    }
    return render(request, "supplier/supplier_dashboard.html", context)

# H - Delete View (Team member can delete)
@user_passes_test(lambda u: not is_azure_admin(u))
@login_required
def delete_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)

    if supplier.created_by != request.user:
        raise PermissionDenied

    query = request.GET.get("q", "").strip()

    if request.method == 'POST':
        name = supplier.name_of_supplier
        supplier.delete()
        messages.success(request, f"🗑️ Supplier '{name}' deleted successfully.")
        return redirect(f"{reverse('supplier_dashboard')}?q={query}")

    return render(request, "supplier/confirm_delete.html", {
        "supplier": supplier,
        "query": query
    })
