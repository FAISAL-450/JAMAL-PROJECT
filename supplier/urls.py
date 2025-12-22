from django.urls import path
from . import views

urlpatterns = [
    # 🔹 Team dashboard: team members manage their own team's suppliers
    path('dashboard/', views.supplier_dashboard, name='supplier_dashboard'),

    # 🔹 Admin dashboard: Azure admin views all supplier records
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),

    # ✏️ Edit supplier entry (Team member can edit)
    path('dashboard/edit/<int:pk>/', views.edit_supplier, name='edit_supplier'),

    # 🗑️ Delete supplier entry (Team member can delete)
    path('dashboard/delete/<int:pk>/', views.delete_supplier, name='delete_supplier'),
]
