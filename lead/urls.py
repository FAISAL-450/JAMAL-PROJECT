from django.urls import path
from . import views

urlpatterns = [
    # 🔹 Team dashboard: team members manage their own team's leads
    path('dashboard/', views.lead_dashboard, name='lead_dashboard'),

    # 🔹 Admin dashboard: Azure admin views all leads records
    path('dashboard/admin/', views.admin_dashboard, name='lead_admin_dashboard'),

    # ✏️ Edit lead entry (only owner, not Azure admin)
    path('dashboard/edit/<int:pk>/', views.edit_lead, name='edit_lead'),

    # 🗑️ Delete lead entry (only owner, not Azure admin)
    path('dashboard/delete/<int:pk>/', views.delete_lead, name='delete_lead'),

    # 🔄 Auto-fill API endpoint
    path('dashboard/get-customer-details/<int:customerId>/', views.get_customer_details, name='get_customer_details'),

]
