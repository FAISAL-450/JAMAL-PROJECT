from django.urls import path
from . import views

urlpatterns = [
    # 🔹 Team dashboard: team members manage their own chloride test records
    path('dashboard/', views.chloridetest_dashboard, name='chloridetest_dashboard'),

    # 🔹 Admin dashboard: Azure admin views all chloride test records
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),

    # ✏️ Edit chloride test entry (only owner or admin with permission)
    path('dashboard/edit/<int:pk>/', views.edit_chloride_test, name='edit_chloride_test'),

    # 🗑️ Delete chloride test entry (only owner or admin with permission)
    path('dashboard/delete/<int:pk>/', views.delete_chloride_test, name='delete_chloride_test'),

    # 📩 Team member requests edit/delete access
    path('dashboard/request/<int:pk>/', views.request_team_permission, name='request_team_permission'),

    # ✅ Admin approves edit/delete access
    path('dashboard/admin/approve/<int:pk>/', views.approve_team_permission, name='approve_team_permission'),
]





