# A - Import Required Modules
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied

from .models import Project
from .forms import ProjectForm   # <-- assumes you created a ProjectForm

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

# E - Unified Dashboard View
@login_required
def project_dashboard(request):
    query = request.GET.get("q", "").strip()
    name_of_project = request.GET.get("name_of_project", "").strip()
    project_address = request.GET.get("project_address", "").strip()

    form = ProjectForm(request.POST or None)
    is_admin = is_azure_admin(request.user)

    # Apply filtering function with all parameters
    projects = filter_projects(
        query=query,
        user=request.user if not is_admin else None,
        name_of_project=name_of_project if name_of_project else None,
        project_address=project_address if project_address else None
    )
    projects_page = get_paginated_queryset(request, projects)

    # Handle project creation for non-admins
    if not is_admin and request.method == "POST" and form.is_valid():
        project = form.save(commit=False)
        project.created_by = request.user
        profile = getattr(request.user, "project_profile", None)
        project.team = getattr(profile, "role", "manager")
        project.save()
        messages.success(request, "✅ Project record created successfully.")
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
        "readonly": is_admin,
        "is_admin": is_admin,
        "current_user": request.user,
    }
    return render(request, "project/project_dashboard.html", context)

# F - Admin Dashboard View
@user_passes_test(is_azure_admin)
@login_required
def project_admin_dashboard(request):
    # Extract filters from GET params
    query = request.GET.get("q", "").strip()
    name_of_project = request.GET.get("name_of_project", "").strip()
    project_address = request.GET.get("project_address", "").strip()

    # Use unified filter function
    projects = filter_projects(
        query=query if query else None,
        name_of_project=name_of_project if name_of_project else None,
        project_address=project_address if project_address else None
    )

    projects_page = get_paginated_queryset(request, projects)

    context = {
        "projects": projects_page,
        "query": query,
        "name_of_project": name_of_project,
        "project_address": project_address,
        "form": ProjectForm(),
        "mode": "admin",
        "readonly": True,
        "is_admin": True,
        "current_user": request.user,
    }
    return render(request, "project/project_dashboard.html", context)

# G - Edit View
@login_required
def project_edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    is_admin = is_azure_admin(request.user)

    if not (is_admin or (project.created_by == request.user and project.allow_team_edit)):
        raise PermissionDenied

    query = request.GET.get("q", "").strip()
    form = ProjectForm(request.POST or None, instance=project)

    if form.is_valid():
        updated_project = form.save(commit=False)
        updated_project.updated_by = request.user

        # 👇 Reset team permission after edit
        if not is_admin:
            updated_project.allow_team_edit = False
            updated_project.edit_request_pending = False

        updated_project.save()
        messages.success(request, "✏️ Project record updated successfully.")
        redirect_url = 'project_admin_dashboard' if is_admin else 'project_dashboard'
        return redirect(f"{reverse(redirect_url)}?q={query}")

    projects = filter_projects(query=query, user=request.user if not is_admin else None)
    projects_page = get_paginated_queryset(request, projects)

    context = {
        "form": form,
        "mode": "edit",
        "project": project,
        "query": query,
        "projects": projects_page,
        "readonly": is_admin,
        "is_admin": is_admin,
        "current_user": request.user
    }
    return render(request, "project/project_dashboard.html", context)

# H - Delete View
@login_required
def project_delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    is_admin = is_azure_admin(request.user)

    if not (is_admin or (project.created_by == request.user and project.allow_team_edit)):
        raise PermissionDenied

    query = request.GET.get("q", "").strip()

    if request.method == 'POST':
        name = project.name_of_project
        project.delete()
        messages.success(request, f"🗑️ Project '{name}' deleted successfully.")
        redirect_url = 'project_admin_dashboard' if is_admin else 'project_dashboard'
        return redirect(f"{reverse(redirect_url)}?q={query}")

    return render(request, "project/confirm_delete.html", {
        "project": project,
        "query": query
    })

# I - Admin Approves Edit/Delete Request
@user_passes_test(is_azure_admin)
@login_required
def project_approve_team_permission(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.allow_team_edit = True
    project.edit_request_pending = False
    project.updated_by = request.user
    project.save()
    messages.success(request, f"✅ Edit/delete permission granted for '{project.name_of_project}'. Team member can now proceed.")
    return redirect(reverse('project_admin_dashboard'))

# J - Team Member Requests Edit/Delete Access
@login_required
def project_request_team_permission(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if project.created_by != request.user:
        raise PermissionDenied

    if not project.edit_request_pending:
        project.edit_request_pending = True
        project.save()
        messages.success(request, f"📩 Request sent to admin for '{project.name_of_project}'. Awaiting approval.")
    else:
        messages.info(request, f"⏳ Request already pending for '{project.name_of_project}'.")

    return redirect(reverse('project_dashboard'))
