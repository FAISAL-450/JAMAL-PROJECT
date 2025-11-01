from django.urls import path
from . import views
app_name = 'salesmarketing'  # Namespace for reverse URL resolution
urlpatterns = [
    path('customerdetailed-detailed/', views.salesmarketing_doc_list, name='salesmarketing_doc_list'),
    path('lead-detailed/', views.salesmarketing_ld_list, name='salesmarketing_ld_list'),
    
]
