from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from customerdetailed.models import CustomerDetailed

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

# 🏗️ Sales & Marketing Customer Detailed List View
def salesmarketing_doc_list(request):
    query = request.GET.get('q', '').strip()
    customerdetaileds = CustomerDetailed.objects.filter(department='salesmarketing')
    if query:
        customerdetaileds = customerdetaileds.filter(name__icontains=query)

    customerdetaileds_page = get_paginated_queryset(request, customerdetaileds, per_page=10)

    return render(request, 'salesmarketing/salesmarketing_doc_list.html', {
        'customerdetaileds': customerdetaileds_page,
        'query': query
    })

# 🏗️ Sales & Marketing Customer Bill Detailed List View
def salesmarketing_cb_list(request):
    query = request.GET.get('q', '').strip()

    customerbills = Customerbill.objects.filter(department='salesmarketing')
    
    if query:
        customerbills = customerbills.filter(customer_name__icontains=query)

    customerbills_page = get_paginated_queryset(request, customerbills, per_page=10)

    return render(request, 'salesmarketing/salesmarketing_cb_list.html', {
        'customerbills': customerbills_page,
        'query': query
    })

# 🏗️ Sales & Marketing Proposal Document Detailed List View
def salesmarketing_pc_list(request):
    query = request.GET.get('q', '').strip()

    proposals = Proposal.objects.filter(department='salesmarketing')
    
    if query:
        proposals = proposals.filter(title__icontains=query)

    proposals_page = get_paginated_queryset(request, proposals, per_page=10)

    return render(request, 'salesmarketing/salesmarketing_pc_list.html', {
        'proposals': proposals_page,
        'query': query
    })
