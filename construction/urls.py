from django.urls import path
from . import views
app_name = 'construction'  # Namespace for reverse URL resolution
urlpatterns = [
    path('project-detailed/', views.construction_pd_list, name='construction_pd_list'),
    path('contractor-detailed/', views.construction_cd_list, name='construction_cd_list'),
    
    path('ct-detailed/', views.construction_ct_list, name='construction_ct_list'),
    path('requisition-detailed/', views.construction_pr_list, name='construction_pr_list'),
    path('contractorbill-detailed/', views.construction_cb_list, name='construction_cb_list'),

]
