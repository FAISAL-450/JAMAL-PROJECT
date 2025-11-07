from django.urls import path
from . import views

urlpatterns = [
    # 📋 Team Dashboard View-(list + create)
    path('dashboard/', views.project_dashboard, name='project_dashboard'),

    # 🛡️ Admin Dashboard View-(read-only)
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),

    # ✏️ Edit Project View-(owner or team member)
    path('dashboard/edit/<int:pk>/', views.edit_project, name='edit_project'),

    # 🗑️ Delete Project View-(owner or team member)
    path('dashboard/delete/<int:pk>/', views.delete_project, name='delete_project'),
]




