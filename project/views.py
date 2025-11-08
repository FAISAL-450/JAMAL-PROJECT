# A - Import Required Modules
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied

from .models import Project
from .forms import ProjectForm

# B - Azure Admin Check
AZURE_ADMIN_EMAIL = 'admin@dzignscapeprofessionals.onmicrosoft.com'

def is_azure_admin(user):
    return getattr(user, 'email', '').lower() == AZURE_ADMIN_EMAIL.lower()

# C - Filtering Function
def filter_projects(query=None, user=None, exclude_user=None):
    queryset = Project.objects.all()

    if user:
        queryset = queryset.filter(created_by=user)

    if exclude_user:
        queryset = queryset.exclude(created_by=exclude_user)

    if query:
        queryset = queryset.filter(
            Q(name_of_project__icontains=query) |
            Q(project_address__icontains=query) |
            Q(contact_person_name__icontains=query)
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

# E - Unified Dashboard View (List View + Form Submission)
@login_required
def project_dashboard(request):
    query = request.GET.get("q", "").strip()
    form = ProjectForm(request.POST or None)

    if is_azure_admin(request.user):
        projects = filter_projects(query=query)
    else:
        projects = filter_projects(query=query, user=request.user)

    projects_page = get_paginated_queryset(request, projects)

    if not is_azure_admin(request.user) and request.method == "POST" and form.is_valid():
        project = form.save(commit=False)
        project.created_by = request.user
        project.save()
        messages.success(request, "✅ Project created successfully.")
        return redirect(f"{reverse('project_dashboard')}?q={query}")

    return render(request, "project/project_dashboard.html", {
        "projects": projects_page,
        "query": query,
        "form": form,
        "mode": "list",
        "readonly": is_azure_admin(request.user)
    })

# F - Admin Dashboard View (Azure Admin only, read-only)
@user_passes_test(is_azure_admin)
def admin_project_dashboard(request):
    query = request.GET.get("q", "").strip()
    projects = filter_projects(query=query)
    projects_page = get_paginated_queryset(request, projects)

    return render(request, "project/project_dashboard.html", {
        "projects": projects_page,
        "query": query,
        "form": ProjectForm(),
        "mode": "admin",
        "readonly": True
    })

# G - Edit View (Only owner can edit)
@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if project.created_by != request.user:
        raise PermissionDenied

    query = request.GET.get("q", "").strip()
    form = ProjectForm(request.POST or None, instance=project)

    if form.is_valid():
        form.save()
        messages.success(request, "✏️ Project updated successfully.")
        return redirect(f"{reverse('project_dashboard')}?q={query}")

    projects = filter_projects(query=query, user=request.user)
    projects_page = get_paginated_queryset(request, projects)

    return render(request, "project/project_dashboard.html", {
        "form": form,
        "mode": "edit",
        "project": project,
        "query": query,
        "projects": projects_page,
        "readonly": False
    })

# H - Delete View (Only owner can delete)
@login_required
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if project.created_by != request.user:
        raise PermissionDenied

    query = request.GET.get("q", "").strip()

    if request.method == 'POST':
        name = project.name_of_project
        project.delete()
        messages.success(request, f"🗑️ Project '{name}' deleted successfully.")
        return redirect(f"{reverse('project_dashboard')}?q={query}")

    return render(request, "project/confirm_delete.html", {
        "project": project,
        "query": query
    })




