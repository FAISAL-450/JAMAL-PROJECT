# A - Import Required Modules
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .models import Project
from .forms import ProjectForm

# B - Azure Admin Check
def is_azure_admin(user):
    return user.email.lower() == 'admin@dzignscapeprofessionals.onmicrosoft.com'

# C - Filtering Function
def filter_projects(query=None, user=None, admin_view=False):
    queryset = Project.objects.all()

    if not admin_view and user:
        queryset = queryset.filter(created_by=user)

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

# E - Team Member Dashboard View
@login_required
def project_dashboard(request):
    query = request.GET.get("q", "").strip()
    is_admin = is_azure_admin(request.user)

    projects = filter_projects(query=query, user=request.user, admin_view=is_admin)
    projects_page = get_paginated_queryset(request, projects)

    form = ProjectForm(request.POST or None) if not is_admin else None

    if not is_admin and request.method == "POST" and form.is_valid():
        project = form.save(commit=False)
        project.created_by = request.user
        project.team = getattr(request.user.project_profile, "role", None)
        project.save()
        messages.success(request, "✅ Project created successfully.")
        return redirect(f"{reverse('project_dashboard')}?q={query}")

    return render(request, "project/project_dashboard.html", {
        "projects": projects_page,
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
    projects = filter_projects(query=query, admin_view=True)
    projects_page = get_paginated_queryset(request, projects)

    return render(request, "project/project_dashboard.html", {
        "projects": projects_page,
        "query": query,
        "form": None,
        "mode": "admin",
        "readonly": True
    })

# G - Edit View (Only team member can edit their own)
@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if is_azure_admin(request.user) or project.created_by != request.user:
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

# H - Delete View (Only team member can delete their own)
@login_required
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if is_azure_admin(request.user) or project.created_by != request.user:
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




