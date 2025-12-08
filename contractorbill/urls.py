from django.urls import path
from . import views

urlpatterns = [
    # 🔹 Team dashboard: team members manage their own contractor bills
    path('dashboard/', views.contractorbill_dashboard, name='contractorbill_dashboard'),

    # 🔹 Admin dashboard: Azure admin views all contractor bill records
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),

    # ✏️ Edit contractor bill entry (Team member can edit)
    path('dashboard/edit/<int:pk>/', views.edit_contractorbill, name='edit_contractorbill'),

    # 🗑️ Delete contractor bill entry (Team member can delete)
    path('dashboard/delete/<int:pk>/', views.delete_contractorbill, name='delete_contractorbill'),

    # 🔎 Auto-fill API endpoint (used by JavaScript)
    path('dashboard/get_contractorbill_details/<int:pk>/', views.get_contractorbill_details, name='get_contractorbill_details'),
]
