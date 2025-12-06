from django.urls import path
from . import views

app_name = "project"  # enables namespacing in templates

urlpatterns = [
    # Team dashboard
    path("dashboard/", views.project_dashboard, name="project_dashboard"),

    # Admin dashboard
    path("dashboard/admin/", views.admin_dashboard, name="admin_dashboard"),

    # Edit project
    path("edit/<int:pk>/", views.edit_project, name="edit_project"),

    # Delete project
    path("delete/<int:pk>/", views.delete_project, name="delete_project"),

    # Request edit/delete permission
    path("request/<int:pk>/", views.request_team_permission, name="request_team_permission"),

    # Admin approves permission
    path("admin/approve/<int:pk>/", views.approve_team_permission, name="approve_team_permission"),
]

















