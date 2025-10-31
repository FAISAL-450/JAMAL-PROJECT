# A - Import Required Modules
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse
from django.db.models import Q
from django.contrib import messages
from .models import Account
from .forms import AccountForm

# B - Filtering Function
def filter_accounts(query=None):
    queryset = Account.objects.all()
    if query:
        queryset = queryset.filter(Q(account_name__icontains=query))
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

# D - Unified View (List View + Form Submission)
def account_dashboard(request):
    query = request.GET.get("q", "").strip()
    accounts = filter_accounts(query)
    accounts_page = get_paginated_queryset(request, accounts, per_page=10)

    form = AccountForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        account = form.save(commit=False)
        account.save()
        messages.success(request, "✅ Account created successfully.")
        return redirect(f"{reverse('account_dashboard')}?q={query}")

    return render(request, "account/account_dashboard.html", {
        "accounts": accounts_page,
        "query": query,
        "form": form,
        "mode": "list"
    })

# E - Edit View (Inline Form + List Table)
def edit_account(request, pk):
    account = get_object_or_404(Account, pk=pk)
    query = request.GET.get("q", "").strip()

    form = AccountForm(request.POST or None, instance=account)
    if form.is_valid():
        form.save()
        messages.success(request, "✏️ Account updated successfully.")
        return redirect(f"{reverse('account_dashboard')}?q={query}")

    accounts = filter_accounts(query)
    accounts_page = get_paginated_queryset(request, accounts, per_page=10)

    return render(request, "account/account_dashboard.html", {
        "form": form,
        "mode": "edit",
        "account": account,
        "query": query,
        "accounts": accounts_page
    })

# F - Delete View (Confirmation + Redirect)
def account_delete(request, pk):
    account = get_object_or_404(Account, pk=pk)
    query = request.GET.get("q", "").strip()

    if request.method == 'POST':
        name = account.account_name
        account.delete()
        messages.success(request, f"🗑️ Account '{name}' deleted successfully.")
        return redirect(f"{reverse('account_dashboard')}?q={query}")
