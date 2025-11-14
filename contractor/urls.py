from django.urls import path
from . import views

urlpatterns = [
    # 🔹 Team dashboard: team members manage their own team's contractors
    path('dashboard/', views.contractor_dashboard, name='contractor_dashboard'),

    # 🔹 Admin dashboard: Azure admin views all contractor records
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),

    # ✏️ Edit contractor entry (only owner, not Azure admin)
    path('dashboard/edit/<int:pk>/', views.edit_contractor, name='edit_contractor'),

    # 🗑️ Delete contractor entry (only owner, not Azure admin)
    path('dashboard/delete/<int:pk>/', views.delete_contractor, name='delete_contractor'),
]
