from django.urls import path
from . import views

urlpatterns = [
    # ✅ Unified Dashboard (Admin + Team Member)
    path("dashboard/", views.contractorbill_dashboard, name="contractorbill_dashboard"),

    # ✅ Edit View (Admin can edit all, team only their own)
    path("dashboard/edit/<int:pk>/", views.edit_contractorbill, name="edit_contractorbill"),

    # ✅ Delete View (Admin can delete all, team only their own)
    path("dashboard/delete/<int:pk>/", views.delete_contractorbill, name="delete_contractorbill"),


# 🔎 Auto-fill API endpoint (used by JavaScript)
    path('dashboard/get_contractorbill_details/<int:pk>/', views.get_contractorbill_details, name='get_contractorbill_details'),
]
