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
from .models import CustomerDetailed

# B - Filtering Function
def filter_leads(query=None, user=None, exclude_user=None):
    queryset = Lead.objects.select_related('customer_name').all()

    if user:
        queryset = queryset.filter(customer_name__created_by=user)

    if exclude_user:
        queryset = queryset.exclude(customer_name__created_by=exclude_user)

    if query:
        queryset = queryset.filter(
            Q(customer_name__name__icontains=query) |
            Q(customer_email__icontains=query) |
            Q(customer_company__icontains=query)
        )

    return queryset

# C - Reusable Pagination Function
def get_paginated_queryset(request, queryset, per_page=10):
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get("page")

    try:
        return paginator.page(page_number)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)

# D - Unified Dashboard View (List View + Form Submission)
@login_required
def lead_dashboard(request):
    query = request.GET.get("q", "").strip()
    form = LeadForm(request.POST or None, user=request.user)

    # Role-based filtering
    if request.user.email == 'admin@dzignscapeprofessionals.onmicrosoft.com':
        leads = filter_leads(query=query, exclude_user=request.user)
    else:
        leads = filter_leads(query=query, user=request.user)

    leads_page = get_paginated_queryset(request, leads)

    # Save logic: only Based and Dulal can submit
    if request.user.email in ['based@dzignscapeprofessionals.onmicrosoft.com', 'dulal@dzignscapeprofessionals.onmicrosoft.com'] and request.method == "POST" and form.is_valid():
        lead = form.save(commit=False)
        lead.save()
        messages.success(request, "✅ Lead record created successfully.")
        return redirect(f"{reverse('lead_dashboard')}?q={query}")

    return render(request, "lead/lead_dashboard.html", {
        "leads": leads_page,
        "query": query,
        "form": form,
        "mode": "list",
        "readonly": request.user.email == 'admin@dzignscapeprofessionals.onmicrosoft.com'
    })

# E - Admin Dashboard View (Admin only, read-only)
@user_passes_test(lambda u: u.email == 'admin@dzignscapeprofessionals.onmicrosoft.com')
def lead_admin_dashboard(request):
    query = request.GET.get("q", "").strip()
    leads = filter_leads(query=query, exclude_user=request.user)
    leads_page = get_paginated_queryset(request, leads)

    return render(request, "lead/lead_dashboard.html", {
        "leads": leads_page,
        "query": query,
        "form": LeadForm(user=request.user),   # Admin can view form but not submit
        "mode": "admin",
        "readonly": True
    })

# F - Edit View (Only owner can edit)
@login_required
def edit_lead(request, pk):
    lead = get_object_or_404(Lead, pk=pk)

    if lead.customer_name.created_by != request.user or request.user.email == 'admin@dzignscapeprofessionals.onmicrosoft.com':
        raise PermissionDenied

    query = request.GET.get("q", "").strip()
    form = LeadForm(request.POST or None, instance=lead, user=request.user)

    if form.is_valid():
        form.save()
        messages.success(request, "✏️ Lead record updated successfully.")
        return redirect(f"{reverse('lead_dashboard')}?q={query}")

    leads = filter_leads(query=query, user=request.user)
    leads_page = get_paginated_queryset(request, leads)

    return render(request, "lead/lead_dashboard.html", {
        "form": form,
        "mode": "edit",
        "lead": lead,
        "query": query,
        "leads": leads_page,
        "readonly": False
    })

# G - Delete View (Only owner can delete)
@login_required
def lead_delete(request, pk):
    lead = get_object_or_404(Lead, pk=pk)

    if lead.customer_name.created_by != request.user or request.user.email == 'admin@dzignscapeprofessionals.onmicrosoft.com':
        raise PermissionDenied

    query = request.GET.get("q", "").strip()

    if request.method == 'POST':
        name = lead.customer_name.name if lead.customer_name else "Unnamed"
        lead.delete()
        messages.success(request, f"🗑️ Lead '{name}' deleted successfully.")
        return redirect(f"{reverse('lead_dashboard')}?q={query}")

    return render(request, "lead/confirm_delete.html", {
        "lead": lead,
        "query": query
    })

# H - Auto-Fill API View (used by JavaScript)
def get_customer_details(request, pk):
    customer = get_object_or_404(CustomerDetailed, pk=pk)
    return JsonResponse({
        'email': customer.email or '',
        'phone': customer.phone or '',
        'company': customer.company or '',
    })

