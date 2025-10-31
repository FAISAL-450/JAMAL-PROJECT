# A - Import Required Modules
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse
from django.db.models import Q
from django.contrib import messages
from .models import Project
from .forms import ProjectForm

# B - Filtering Function
def filter_projects(query=None):
    queryset = Project.objects.all()
    if query:
        queryset = queryset.filter(Q(name_of_project__icontains=query))
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
def project_dashboard(request):
    query = request.GET.get("q", "").strip()
    projects = filter_projects(query)
    projects_page = get_paginated_queryset(request, projects, per_page=10)

    form = ProjectForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        project = form.save(commit=False)
        project.save()
        messages.success(request, "✅ Project created successfully.")
        return redirect(f"{reverse('project_dashboard')}?q={query}")

    return render(request, "project/project_dashboard.html", {
        "projects": projects_page,
        "query": query,
        "form": form,
        "mode": "list"
    })

# E - Edit View (Inline Form + List Table)
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    query = request.GET.get("q", "").strip()

    form = ProjectForm(request.POST or None, instance=project)
    if form.is_valid():
        form.save()
        messages.success(request, "✏️ Project updated successfully.")
        return redirect(f"{reverse('project_dashboard')}?q={query}")
    projects = filter_projects(query)
    projects_page = get_paginated_queryset(request, projects, per_page=10)
    return render(request, "project/project_dashboard.html", {
        "form": form,
        "mode": "edit",
        "project": project,
        "query": query,
        "projects": projects_page
    })

# F - Delete View (Confirmation + Redirect)
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    query = request.GET.get("q", "").strip()

    if request.method == 'POST':
        project_name = project.name_of_project
        project.delete()
        messages.success(request, f"🗑️ Project '{project_name}' deleted successfully.")
        return redirect(f"{reverse('project_dashboard')}?q={query}")
