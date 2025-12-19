from django.urls import path
from . import views

urlpatterns = [
    # 🔹 Team dashboard: team members manage their own PR records
    path('dashboard/', views.pr_dashboard, name='pr_dashboard'),

    # 🔹 Admin dashboard: Azure admin views all PR records
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),

    # ✏️ Edit PR entry (Team member can edit)
    path('dashboard/edit/<int:pk>/', views.edit_pr, name='edit_pr'),

    # 🗑️ Delete PR entry (Team member can delete)
    path('dashboard/delete/<int:pk>/', views.delete_pr, name='delete_pr'),

    # 📤 Submit PR for approval (team)
    path('dashboard/submit/<int:pk>/', views.submit_pr_for_approval, name='submit_pr_for_approval'),

    # ✅ Approve PR (admin)
    path('dashboard/approve/<int:pk>/', views.approve_pr, name='approve_pr'),

    # 🔎 Auto-fill API endpoint (used by JavaScript)
    path('dashboard/get_pr_details/<int:pk>/', views.get_pr_details, name='get_pr_details'),

]
