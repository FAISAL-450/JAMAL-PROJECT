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
    return user.email in {
        'admin@dzignscapeprofessionals.onmicrosoft.com',
        'based@dzignscapeprofessionals.onmicrosoft.com'
    }

# C - Filtering Function
def filter_projects(query=None, user=None, is_admin=False):
    queryset = Project.objects.all()

    # Team members (non-admins) only see their own records
    if not is_admin and user:
        queryset = queryset.filter(created_by=user)

    if query:
        queryset = queryset.filter(
            Q(name_of_project__icontains=query) |
            Q(project_address__icontains=query) |
            Q(contact_person_name__icontains=query)
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

# E - Unified Dashboard View (List View + Form Submission)
@login_required
def project_dashboard(request):
    query = request.GET.get("q", "").strip()
    form = ProjectForm(request.POST or None)
    is_admin = is_azure_admin(request.user)

    projects = filter_projects(query=query, user=request.user, is_admin=is_admin)
    projects_page = get_paginated_queryset(request, projects)

    if request.method == "POST" and form.is_valid():
        project = form.save(commit=False)
        project.created_by = request.user
        project.team = getattr(
            getattr(request.user, "project_profile", None),
            "role",
            "manager"   # <-- updated default role
        )
        project.save()
        messages.success(request, "✅ Project detailed record created successfully.")
        return redirect(f"{reverse('project_dashboard')}?q={query}")

    context = {
        "projects": projects_page,
        "query": query,
        "form": form,
        "mode": "list",
        "readonly": False,
        "is_admin": is_admin
    }
    return render(request, "project/project_dashboard.html", context)

# F - Edit View (Admin can edit all, team members only their own)
@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    is_admin = is_azure_admin(request.user)

    if not is_admin and project.created_by != request.user:
        raise PermissionDenied

    query = request.GET.get("q", "").strip()
    form = ProjectForm(request.POST or None, instance=project)

    if form.is_valid():
        form.save()
        messages.success(request, "✏️ Project detailed record updated successfully.")
        return redirect(f"{reverse('project_dashboard')}?q={query}")

    projects = filter_projects(query=query, user=request.user, is_admin=is_admin)
    projects_page = get_paginated_queryset(request, projects)

    context = {
        "form": form,
        "mode": "edit",
        "project": project,
        "query": query,
        "projects": projects_page,
        "readonly": False,
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
