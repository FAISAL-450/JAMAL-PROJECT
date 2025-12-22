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

# 🏗️ Construction Chloride Test List View
def construction_ct_list(request):
    query = request.GET.get('q', '').strip()
    chloridetests = ChlorideTest.objects.filter(department='construction')

    if query:
        chloridetests = chloridetests.filter(time_interval_min__icontains=query)

    chloridetests_page = get_paginated_queryset(request, chloridetests, per_page=10)

    return render(request, 'construction/construction_ct_list.html', {
        'chloridetests': chloridetests_page,
        'query': query
    })

# 🏗️ Construction Requisition List View
def construction_pr_list(request):
    query = request.GET.get('q', '').strip()
    requisitions = Requisition.objects.filter(department='construction')

    if query:
        requisitions = requisitions.filter(pr_no__icontains=query)

    requisitions_page = get_paginated_queryset(request, requisitions, per_page=10)

    return render(request, 'construction/construction_pr_list.html', {
        'requisitions': requisitions_page,
        'query': query
    })

# 🏗️ Construction Contractor Bill List View
def construction_cb_list(request):
    query = request.GET.get('q', '').strip()
    contractorbills = Contractorbill.objects.filter(department='construction')

    if query:
        contractorbills = contractorbills.filter(contractor_company_name__icontains=query)

    contractorbills_page = get_paginated_queryset(request, contractorbills, per_page=10)

    return render(request, 'construction/construction_cb_list.html', {
        'contractorbills': contractorbills_page,
        'query': query
    })

# 🏗️ Construction Resource List View
def construction_rl_list(request):
    query = request.GET.get('q', '').strip()
    resources = Resource.objects.filter(department='construction')  

    if query:
        resources = resources.filter(name_of_resource__icontains=query)

    resources_page = get_paginated_queryset(request, resources, per_page=10)

    return render(request, 'construction/construction_rl_list.html', {
        'resources': resources_page,
        'query': query
    })

# 🏗️ Construction PR List View
def construction_ppr_list(request):
    query = request.GET.get('q', '').strip()
    prs = Pr.objects.filter(department='construction')  

    if query:
        prs = prs.filter(resource_name_pr__icontains=query)

    prs_page = get_paginated_queryset(request, prs, per_page=10)

    return render(request, 'construction/construction_ppr_list.html', {
        'prs': prs_page,
        'query': query
    })

# 🏗️ Construction Supplier List View
def construction_sl_list(request):
    query = request.GET.get('q', '').strip()
    suppliers = Supplier.objects.filter(department='construction')  

    if query:
        suppliers = suppliers.filter(name_of_supplier__icontains=query)

    suppliers_page = get_paginated_queryset(request, suppliers, per_page=10)

    return render(request, 'construction/construction_sl_list.html', {
        'suppliers': suppliers_page,
        'query': query
    })
