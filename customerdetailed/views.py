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

# E - Unified Dashboard View
@login_required
def customerdetailed_dashboard(request):
    query = request.GET.get("q", "").strip()
    form = CustomerDetailedForm(request.POST or None)
    is_admin = is_azure_admin(request.user)

    customerdetaileds = filter_customerdetaileds(query=query, user=request.user if not is_admin else None)
    customerdetaileds_page = get_paginated_queryset(request, customerdetaileds)

    if not is_admin and request.method == "POST" and form.is_valid():
        customer = form.save(commit=False)
        customer.created_by = request.user
        profile = getattr(request.user, "customerdetailed_profile", None)
        customer.team = getattr(profile, "role", "support")
        customer.save()
        messages.success(request, "✅ Customer detailed record created successfully.")
        return redirect(f"{reverse('customerdetailed_dashboard')}?q={query}")

    context = {
        "customerdetaileds": customerdetaileds_page,
        "query": query,
        "form": form,
        "mode": "list",
        "readonly": is_admin,
        "is_admin": is_admin,
        "current_user": request.user
    }
    return render(request, "customerdetailed/customerdetailed_dashboard.html", context)

# F - Admin Dashboard View
@user_passes_test(is_azure_admin)
@login_required
def admin_dashboard(request):
    query = request.GET.get("q", "").strip()
    customerdetaileds = CustomerDetailed.objects.all()

    if query:
        customerdetaileds = customerdetaileds.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(company__icontains=query)
        )

    customerdetaileds_page = get_paginated_queryset(request, customerdetaileds)

    context = {
        "customerdetaileds": customerdetaileds_page,
        "query": query,
        "form": CustomerDetailedForm(),
        "mode": "admin",
        "readonly": True,
        "is_admin": True,
        "current_user": request.user
    }
    return render(request, "customerdetailed/customerdetailed_dashboard.html", context)

# G - Edit View
@login_required
def edit_customer(request, pk):
    customer = get_object_or_404(CustomerDetailed, pk=pk)
    is_admin = is_azure_admin(request.user)

    if not (is_admin or (customer.created_by == request.user and customer.allow_team_edit)):
        raise PermissionDenied

    query = request.GET.get("q", "").strip()
    form = CustomerDetailedForm(request.POST or None, instance=customer)

    if form.is_valid():
        updated_customer = form.save(commit=False)
        updated_customer.updated_by = request.user
        updated_customer.save()
        messages.success(request, "✏️ Customer detailed record updated successfully.")
        redirect_url = 'admin_dashboard' if is_admin else 'customerdetailed_dashboard'
        return redirect(f"{reverse(redirect_url)}?q={query}")

    customerdetaileds = filter_customerdetaileds(query=query, user=request.user if not is_admin else None)
    customerdetaileds_page = get_paginated_queryset(request, customerdetaileds)

    context = {
        "form": form,
        "mode": "edit",
        "customer": customer,
        "query": query,
        "customerdetaileds": customerdetaileds_page,
        "readonly": is_admin,
        "is_admin": is_admin,
        "current_user": request.user
    }
    return render(request, "customerdetailed/customerdetailed_dashboard.html", context)

# H - Delete View
@login_required
def delete_customer(request, pk):
    customer = get_object_or_404(CustomerDetailed, pk=pk)
    is_admin = is_azure_admin(request.user)

    if not (is_admin or (customer.created_by == request.user and customer.allow_team_edit)):
        raise PermissionDenied

    query = request.GET.get("q", "").strip()

    if request.method == 'POST':
        name = customer.name
        customer.delete()
        messages.success(request, f"🗑️ Customer '{name}' deleted successfully.")
        redirect_url = 'admin_dashboard' if is_admin else 'customerdetailed_dashboard'
        return redirect(f"{reverse(redirect_url)}?q={query}")

    return render(request, "customerdetailed/confirm_delete.html", {
        "customer": customer,
        "query": query
    })

# I - Admin Approves Edit/Delete Request
@user_passes_test(is_azure_admin)
@login_required
def approve_team_permission(request, pk):
    customer = get_object_or_404(CustomerDetailed, pk=pk)
    customer.allow_team_edit = True
    customer.edit_request_pending = False
    customer.updated_by = request.user
    customer.save()
    messages.success(request, f"✅ Edit/delete permission granted for '{customer.name}'. Team member can now proceed.")
    return redirect(reverse('admin_dashboard'))

# J - Team Member Requests Edit/Delete Access
@login_required
def request_team_permission(request, pk):
    customer = get_object_or_404(CustomerDetailed, pk=pk)

    if customer.created_by != request.user:
        raise PermissionDenied

    if not customer.edit_request_pending:
        customer.edit_request_pending = True
        customer.save()
        messages.success(request, f"📩 Request sent to admin for '{customer.name}'. Awaiting approval.")
    else:
        messages.info(request, f"⏳ Request already pending for '{customer.name}'.")

    return redirect(reverse('customerdetailed_dashboard'))



