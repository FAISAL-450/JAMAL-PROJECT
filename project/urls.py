from django.urls import path
from . import views

urlpatterns = [
    # 🔹 Team dashboard: team members manage their own projects
    path('dashboard/', views.project_dashboard, name='project_dashboard'),

    # 🔹 Admin dashboard: Azure admin views all project records (read-only)
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),

    # ✏️ Edit project entry (only owner, not Azure admin)
    path('dashboard/edit/<int:pk>/', views.edit_project, name='edit_project'),

    # 🗑️ Delete project entry (only owner, not Azure admin)
    path('dashboard/delete/<int:pk>/', views.delete_project, name='delete_project'),
]






