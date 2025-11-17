from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from project.models import Project

# 🔁 Reusable Pagination Function
def get_paginated_queryset(request, queryset, per_page=10):
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get("page")
    try:
        return paginator.page(page_number)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)

# 🏗️ Construction Project List View
def construction_pd_list(request):
    query = request.GET.get('q', '').strip()
    projects = Project.objects.filter(department='construction')
    if query:
        projects = projects.filter(name_of_project__icontains=query)

    projects_page = get_paginated_queryset(request, projects, per_page=10)

    return render(request, 'construction/construction_pd_list.html', {
        'projects': projects_page,
        'query': query
    })

# 🏗️ Construction Contractor List View
def construction_cd_list(request):
    query = request.GET.get('q', '').strip()
    contractors = Contractor.objects.filter(department='construction')

    if query:
        contractors = contractors.filter(contractor_company__icontains=query)

    contractors_page = get_paginated_queryset(request, contractors, per_page=10)

    return render(request, 'construction/construction_cd_list.html', {
        'contractors': contractors_page,
        'query': query
    })

# 🏗️ Construction CTR List View
def construction_ctr_list(request):
    query = request.GET.get('q', '').strip()
    ctrs = Ctr.objects.filter(department='construction')

    if query:
        ctrs = ctrs.filter(time_interval_min__icontains=query)

    ctrs_page = get_paginated_queryset(request, ctrs, per_page=10)

    return render(request, 'construction/construction_ctr_list.html', {
        'ctrs': ctrs_page,
        'query': query
    })
