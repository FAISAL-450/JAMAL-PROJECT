from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.project_dashboard, name='project_dashboard'),
    path('dashboard/edit/<int:pk>/', views.edit_project, name='edit_project'),
    path('dashboard/delete/<int:pk>/', views.project_delete, name='project_delete'),
]
