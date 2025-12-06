# A - Import Required Modules
from django.urls import path
from . import views

# B - URL Patterns
urlpatterns = [
    # 🔹 Team dashboard: team members manage their own projects
    path('dashboard/', views.project_dashboard, name='project_dashboard'),

    # 🔹 Admin dashboard: Azure admin views all project records
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),

    # ✏️ Edit project entry (only owner or admin with permission)
    path('dashboard/edit/<int:pk>/', views.edit_project, name='edit_project'),

    # 🗑️ Delete project entry (only owner or admin with permission)
    path('dashboard/delete/<int:pk>/', views.delete_project, name='delete_project'),

    # 📩 Team member requests edit/delete access
    path('dashboard/request/<int:pk>/', views.request_team_permission, name='request_team_permission'),

    # ✅ Admin approves edit/delete access
    path('dashboard/admin/approve/<int:pk>/', views.approve_team_permission, name='approve_team_permission'),
]






















