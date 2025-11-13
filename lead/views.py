# A - Import Required Modules
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse

from .models import Lead
from .forms import LeadForm
from customerdetailed.models import CustomerDetailed

# B - Azure Admin Check
def is_azure_admin(user):
    return user.email == 'admin@dzignscapeprofessionals.onmicrosoft.com'

# C - Filtering Function
def filter_leads(query=None, user=None, exclude_user=None):
    queryset = Lead.objects.all()

    if user:
        queryset = queryset.filter(created_by=user)

    if exclude_user:
        queryset = queryset.exclude(created_by=exclude_user)

    if query:
        queryset = queryset.filter(
            Q(customer_name__icontains=query) |
            Q(customer_email__icontains=query) |
            Q(customer_phone__icontains=query)
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
def lead_dashboard(request):
    query = request.GET.get("q", "").strip()
    form = LeadForm(request.POST or None)

    # Role-based data filtering
    if is_azure_admin(request.user):
        leads = filter_leads(query=query, exclude_user=request.user)
    else:
        leads = filter_leads(query=query, user=request.user)

    leads_page = get_paginated_queryset(request, leads)
    
    # ✅ Corrected form initialization-(Show-Drop-down-In-Customer Name-Field)
    form = LeadForm(request.POST or None, user=request.user)

    # Save logic: only non-admin users can submit
    if not is_azure_admin(request.user) and request.method == "POST" and form.is_valid():
        lead = form.save(commit=False)
        lead.created_by = request.user
        lead.team = getattr(
            getattr(request.user, "lead_profile", None),
            "role",
            "executive"
        )
        lead.save()
        messages.success(request, "✅ Lead detailed record created successfully.")
        return redirect(f"{reverse('lead_dashboard')}?q={query}")

    context = {
        "leads": leads_page,
        "query": query,
        "form": form,
        "mode": "list",
        "readonly": is_azure_admin(request.user)
    }
    return render(request, "lead/lead_dashboard.html", context)

# F - Admin Dashboard View (Azure Admin only, read-only)
@user_passes_test(is_azure_admin)
@login_required
def admin_dashboard(request):
    query = request.GET.get("q", "").strip()
    leads = filter_leads(query=query, exclude_user=request.user)
    leads_page = get_paginated_queryset(request, leads)

    context = {
        "leads": leads_page,
        "query": query,
        "form": LeadForm(),
        "mode": "admin",
        "readonly": True
    }
    return render(request, "lead/lead_dashboard.html", context)

# G - Edit View (Only owner can edit)
@user_passes_test(lambda u: not is_azure_admin(u))
@login_required
def edit_lead(request, pk):
    lead = get_object_or_404(Lead, pk=pk)

    if lead.created_by != request.user:
        raise PermissionDenied

    query = request.GET.get("q", "").strip()
    form = LeadForm(request.POST or None, instance=lead)

    if form.is_valid():
        form.save()
        messages.success(request, "✏️ Lead detailed record updated successfully.")
        return redirect(f"{reverse('lead_dashboard')}?q={query}")

    leads = filter_leads(query=query, user=request.user)
    leads_page = get_paginated_queryset(request, leads)

    context = {
        "form": form,
        "mode": "edit",
        "lead": lead,
        "query": query,
        "leads": leads_page,
        "readonly": False
    }
    return render(request, "lead/lead_dashboard.html", context)

# H - Delete View (Only owner can delete)
@user_passes_test(lambda u: not is_azure_admin(u))
@login_required
def delete_lead(request, pk):
    lead = get_object_or_404(Lead, pk=pk)

    if lead.created_by != request.user:
        raise PermissionDenied

    query = request.GET.get("q", "").strip()

    if request.method == 'POST':
        name = lead.customer_name
        lead.delete()
        messages.success(request, f"🗑️ Lead '{name}' deleted successfully.")
        return redirect(f"{reverse('lead_dashboard')}?q={query}")

    return render(request, "lead/confirm_delete.html", {
        "lead": lead,
        "query": query
    })

# I - Auto-Fill API View (used by JavaScript)-(Based on-Drop-down- customer_name-Auto-Fill-email, phone, company)
def get_customer_details(request, pk):
    customer = get_object_or_404(CustomerDetailed, pk=pk)
    return JsonResponse({
        'email': customer.email or '',
        'phone': customer.phone or '',
        'company': customer.company or '',
    })

