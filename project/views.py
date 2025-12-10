# A - Import Required Modules
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from urllib.parse import urlencode
from .models import Project
from .forms import ProjectForm

# B - Azure Admin Check
def is_azure_admin(user):
    return user.email == 'admin@dzignscapeprofessionals.onmicrosoft.com'

# C - Filtering Function-(Project Name and Project Address-Based)
def filter_projects(query=None, user=None, exclude_user=None, name_of_project=None, project_address=None):
    queryset = Project.objects.all()

    # User-based filters
    if user:
        queryset = queryset.filter(created_by=user)

    if exclude_user:
        queryset = queryset.exclude(created_by=exclude_user)

    # Free-text search across multiple fields
    if query:
        queryset = queryset.filter(
            Q(name_of_project__icontains=query) |
            Q(project_address__icontains=query)
        )

    # Filter-A: Project Name
    if name_of_project:
        queryset = queryset.filter(name_of_project__icontains=name_of_project)

    # Filter-B: Project Address
    if project_address:
        queryset = queryset.filter(project_address__icontains=project_address)

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

# E - Unified Dashboard View (List View + Form Submission)
@login_required
def project_dashboard(request):
    query = request.GET.get("q", "").strip()
    name_of_project = request.GET.get("name_of_project", "").strip()
    project_address = request.GET.get("project_address", "").strip()
    form = ProjectForm(request.POST or None)

    # Role-based data filtering
    is_admin = is_azure_admin(request.user)
    if is_admin:
        projects = filter_projects(
            query=query,
            exclude_user=request.user,
            name_of_project=name_of_project,
            project_address=project_address
        )
    else:
        projects = filter_projects(
            query=query,
            user=request.user,
            name_of_project=name_of_project,
            project_address=project_address
        )

    projects_page = get_paginated_queryset(request, projects)

    if request.method == "POST" and form.is_valid():
        project = form.save(commit=False)
        project.created_by = request.user
        project.team = getattr(
            getattr(request.user, "project_profile", None),
            "role",
            "manager"   
        )
        project.save()
        messages.success(request, "✅ Project detailed record created successfully.")
        return redirect(
            f"{reverse('project_dashboard')}?q={query}&name_of_project={name_of_project}&project_address={project_address}"
        )

    context = {
        "projects": projects_page,
        "query": query,
        "name_of_project": name_of_project,
        "project_address": project_address,
        "form": form,
        "mode": "list",
        "readonly": False,
        "is_admin": is_admin,
    }
    return render(request, "project/project_dashboard.html", context)

# F - Edit View (Admin can edit all, team members only their own)
@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    is_admin = is_azure_admin(request.user)

    # Permission check: team members can only edit their own
    if not is_admin and project.created_by != request.user:
        raise PermissionDenied

    query = (request.GET.get("q") or "").strip()
    name_of_project = (request.GET.get("name_of_project") or "").strip()
    project_address = (request.GET.get("project_address") or "").strip()

    form = ProjectForm(request.POST or None, instance=project)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "✏️ Project detailed record updated successfully.")
        params = urlencode({
            "q": query,
            "name_of_project": name_of_project,
            "project_address": project_address
        })
        return redirect(f"{reverse('project_dashboard')}?{params}")

    # Build projects list with correct filtering
    if is_admin:
        projects = filter_projects(
            query=query,
            name_of_project=name_of_project,
            project_address=project_address
        )
    else:
        projects = filter_projects(
            query=query,
            user=request.user,
            name_of_project=name_of_project,
            project_address=project_address
        )

    projects_page = get_paginated_queryset(request, projects)

    context = {
        "form": form,
        "mode": "edit",
        "project": project,
        "query": query,
        "name_of_project": name_of_project,
        "project_address": project_address,
        "projects": projects_page,
        "readonly": is_admin,   # consistency
        "is_admin": is_admin
    }
    return render(request, "project/project_dashboard.html", context)

# G - Delete View (Admin can delete all, team members only their own)
@login_required
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    is_admin = is_azure_admin(request.user)

    if not is_admin and project.created_by != request.user:
        raise PermissionDenied

    query = (request.GET.get("q") or "").strip()
    name_of_project = (request.GET.get("name_of_project") or "").strip()
    project_address = (request.GET.get("project_address") or "").strip()

    if request.method == "POST":
        name = project.name_of_project
        project.delete()
        messages.success(request, f"🗑️ Project '{name}' deleted successfully.")
        params = urlencode({
            "q": query,
            "name_of_project": name_of_project,
            "project_address": project_address
        })
        return redirect(f"{reverse('project_dashboard')}?{params}")

    context = {
        "project": project,
        "query": query,
        "name_of_project": name_of_project,
        "project_address": project_address,
        "is_admin": is_admin,
        "readonly": is_admin   # consistency
    }
    return render(request, "project/confirm_delete.html", context)



