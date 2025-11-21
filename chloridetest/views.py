# A - Import Required Modules
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied

from .models import ChlorideTest
from .forms import ChlorideTestForm

# B - Azure Admin Check
def is_azure_admin(user):
    return user.email == 'admin@dzignscapeprofessionals.onmicrosoft.com'

# C - Filtering Function
def filter_chloride_tests(query=None, user=None, exclude_user=None):
    queryset = ChlorideTest.objects.all()

    if user:
        queryset = queryset.filter(created_by=user)

    if exclude_user:
        queryset = queryset.exclude(created_by=exclude_user)

    if query:
        queryset = queryset.filter(
            Q(chloride_ion_permeability__icontains=query) |
            Q(remarks__icontains=query)
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
def chloridetest_dashboard(request):
    query = request.GET.get("q", "").strip()
    form = ChlorideTestForm(request.POST or None)
    is_admin = is_azure_admin(request.user)

    chloride_tests = filter_chloride_tests(query=query, user=request.user if not is_admin else None)
    chloride_tests_page = get_paginated_queryset(request, chloride_tests)

    if not is_admin and request.method == "POST" and form.is_valid():
        test = form.save(commit=False)
        test.created_by = request.user
        profile = getattr(request.user, "chloridetest_profile", None)
        test.team = getattr(profile, "role", "research-manager")
        test.save()
        messages.success(request, "✅ Chloride test record created successfully.")
        return redirect(f"{reverse('chloridetest_dashboard')}?q={query}")

    context = {
        "chloride_tests": chloride_tests_page,
        "query": query,
        "form": form,
        "mode": "list",
        "readonly": is_admin,
        "is_admin": is_admin,
        "current_user": request.user
    }
    return render(request, "chloridetest/chloridetest_dashboard.html", context)

# F - Admin Dashboard View
@user_passes_test(is_azure_admin)
@login_required
def admin_dashboard(request):
    query = request.GET.get("q", "").strip()
    chloride_tests = ChlorideTest.objects.all()

    if query:
        chloride_tests = chloride_tests.filter(
            Q(chloride_ion_permeability__icontains=query) |
            Q(remarks__icontains=query)
        )

    chloride_tests_page = get_paginated_queryset(request, chloride_tests)

    context = {
        "chloride_tests": chloride_tests_page,
        "query": query,
        "form": ChlorideTestForm(),
        "mode": "admin",
        "readonly": True,
        "is_admin": True,
        "current_user": request.user
    }
    return render(request, "chloridetest/chloridetest_dashboard.html", context)

# G - Edit View
@login_required
def edit_chloride_test(request, pk):
    test = get_object_or_404(ChlorideTest, pk=pk)
    is_admin = is_azure_admin(request.user)

    if not (is_admin or (test.created_by == request.user and test.allow_team_edit)):
        raise PermissionDenied

    query = request.GET.get("q", "").strip()
    form = ChlorideTestForm(request.POST or None, instance=test)

    if form.is_valid():
        updated_test = form.save(commit=False)
        updated_test.updated_by = request.user

        # 👇 Reset team permission after edit
        if not is_admin:
            updated_test.allow_team_edit = False
            updated_test.edit_request_pending = False

        updated_test.save()
        messages.success(request, "✏️ Chloride test record updated successfully.")
        redirect_url = 'admin_dashboard' if is_admin else 'chloridetest_dashboard'
        return redirect(f"{reverse(redirect_url)}?q={query}")

    chloride_tests = filter_chloride_tests(query=query, user=request.user if not is_admin else None)
    chloride_tests_page = get_paginated_queryset(request, chloride_tests)

    context = {
        "form": form,
        "mode": "edit",
        "test": test,
        "query": query,
        "chloride_tests": chloride_tests_page,
        "readonly": is_admin,
        "is_admin": is_admin,
        "current_user": request.user
    }
    return render(request, "chloridetest/chloridetest_dashboard.html", context)

# H - Delete View
@login_required
def delete_chloride_test(request, pk):
    test = get_object_or_404(ChlorideTest, pk=pk)
    is_admin = is_azure_admin(request.user)

    if not (is_admin or (test.created_by == request.user and test.allow_team_edit)):
        raise PermissionDenied

    query = request.GET.get("q", "").strip()

    if request.method == 'POST':
        label = f"{test.time_interval_min} min | {test.chloride_ion_permeability}"
        test.delete()
        messages.success(request, f"🗑️ Chloride test '{label}' deleted successfully.")
        redirect_url = 'admin_dashboard' if is_admin else 'chloridetest_dashboard'
        return redirect(f"{reverse(redirect_url)}?q={query}")

    return render(request, "chloridetest/confirm_delete.html", {
        "test": test,
        "query": query
    })

# I - Admin Approves Edit/Delete Request
@user_passes_test(is_azure_admin)
@login_required
def approve_team_permission(request, pk):
    test = get_object_or_404(ChlorideTest, pk=pk)
    test.allow_team_edit = True
    test.edit_request_pending = False
    test.updated_by = request.user
    test.save()
    messages.success(request, f"✅ Edit/delete permission granted for '{test}'. Team member can now proceed.")
    return redirect(reverse('admin_dashboard'))

# J - Team Member Requests Edit/Delete Access
@login_required
def request_team_permission(request, pk):
    test = get_object_or_404(ChlorideTest, pk=pk)

    if test.created_by != request.user:
        raise PermissionDenied

    if not test.edit_request_pending:
        test.edit_request_pending = True
        test.save()
        messages.success(request, f"📩 Request sent to admin for '{test}'. Awaiting approval.")
    else:
        messages.info(request, f"⏳ Request already pending for '{test}'.")

    return redirect(reverse('chloridetest_dashboard'))

