from django.urls import path
from . import views

urlpatterns = [
    # 🔹 Team dashboard: team members manage their own team's projects
    path('dashboard/', views.project_dashboard, name='project_dashboard'),

    # 🔹 Admin dashboard: Azure admin views all project records
    path('dashboard/admin/', views.project_admin_dashboard, name='project_admin_dashboard'),

    # ✏️ Edit project entry (only owner, not Azure admin)
    path('dashboard/edit/<int:pk>/', views.project_edit_project, name='project_edit_project'),

    # 🗑️ Delete project entry (only owner, not Azure admin)
    path('dashboard/delete/<int:pk>/', views.project_delete_project, name='project_delete_project'),

    # 📩 Team member requests edit/delete access
    path('dashboard/request/<int:pk>/', views.project_request_team_permission, name='project_request_team_permission'),

    # ✅ Admin approves edit/delete access
    path('dashboard/admin/approve/<int:pk>/', views.project_approve_team_permission, name='project_approve_team_permission'),
]






















