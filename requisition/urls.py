# A - Import Required Modules
from django.urls import path
from . import views

# B - URL Patterns
urlpatterns = [
    # 🔹 Team dashboard: team members manage their own requisitions
    path('dashboard/', views.requisition_dashboard, name='requisition_dashboard'),

    # 🔹 Admin dashboard: Azure admin views all requisition records
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),

    # ✏️ Edit requisition entry (only owner or admin with permission)
    path('dashboard/edit/<int:pk>/', views.edit_requisition, name='edit_requisition'),

    # 🗑️ Delete requisition entry (only owner or admin with permission)
    path('dashboard/delete/<int:pk>/', views.delete_requisition, name='delete_requisition'),

    # 📩 Team member requests edit/delete access
    path('dashboard/request/<int:pk>/', views.request_team_permission, name='request_team_permission'),

    # ✅ Admin approves edit/delete access
    path('dashboard/admin/approve/<int:pk>/', views.approve_team_permission, name='approve_team_permission'),
]
