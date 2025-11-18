from django.urls import path
from . import views

urlpatterns = [
    # 🔹 Unified dashboard: all users can view and add customer records
    path('dashboard/', views.customerdetailed_dashboard, name='customerdetailed_dashboard'),

    # ✏️ Edit customer entry (owner or Azure admin)
    path('dashboard/edit/<int:pk>/', views.edit_customer, name='edit_customer'),

    # 🗑️ Delete customer entry (owner or Azure admin)
    path('dashboard/delete/<int:pk>/', views.delete_customer, name='delete_customer'),
]
