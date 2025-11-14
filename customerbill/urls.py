from django.urls import path
from . import views

urlpatterns = [
    # 🔹 Team dashboard: team members manage their own team's customer bills
    path('dashboard/', views.customerbill_dashboard, name='customerbill_dashboard'),

    # 🔹 Admin dashboard: Azure admin views all customer bill records
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),

    # ✏️ Edit customer bill entry (only owner, not Azure admin)
    path('dashboard/edit/<int:pk>/', views.edit_customerbill, name='edit_customerbill'),

    # 🗑️ Delete customer bill entry (only owner, not Azure admin)
    path('dashboard/delete/<int:pk>/', views.delete_customerbill, name='delete_customerbill'),
]
