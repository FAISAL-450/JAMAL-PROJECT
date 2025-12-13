from django.urls import path
from . import views

urlpatterns = [
    # 🔹 Team dashboard: team members manage their own team's contractorbills
    path('dashboard/', views.contractorbill_dashboard, name='contractorbill_dashboard'),

    # 🔹 Admin dashboard: Azure admin views all contractorbill records
    path('dashboard/admin/', views.contractorbill_admin_dashboard, name='contractorbill_admin_dashboard'),

    # ✏️ Edit contractorbill entry (only owner, not Azure admin)
    path('dashboard/edit/<int:pk>/', views.contractorbill_edit_contractorbill, name='contractorbill_edit_contractorbill'),

    # 🗑️ Delete contractorbill entry (only owner, not Azure admin)
    path('dashboard/delete/<int:pk>/', views.contractorbill_delete_contractorbill, name='contractorbill_delete_contractorbill'),

    # 📩 Team member requests edit/delete access
    path('dashboard/request/<int:pk>/', views.contractorbill_request_team_permission, name='contractorbill_request_team_permission'),

    # ✅ Admin approves edit/delete access
    path('dashboard/admin/approve/<int:pk>/', views.contractorbill_approve_team_permission, name='contractorbill_approve_team_permission'),

    # 🔎 Auto-fill API endpoint (used by JavaScript)
    path('dashboard/get_contractorbill_details/<int:pk>/', views.get_contractorbill_details, name='get_contractorbill_details'),
]


