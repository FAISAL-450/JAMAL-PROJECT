from django.urls import path
from . import views

urlpatterns = [
    # Unified dashboard view (list + create)
    path('dashboard/', views.project_dashboard, name='project_dashboard'),

    # Admin-only dashboard view
    path('admin-dashboard/', views.admin_project_dashboard, name='admin_project_dashboard'),

    # Edit project view
    path('edit/<int:pk>/', views.edit_project, name='edit_project'),

    # Delete project view
    path('delete/<int:pk>/', views.delete_project, name='delete_project'),
]







