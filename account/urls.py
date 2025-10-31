from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.account_dashboard, name='account_dashboard'),
    path('dashboard/edit/<int:pk>/', views.edit_account, name='edit_account'),
    path('dashboard/delete/<int:pk>/', views.account_delete, name='account_delete'),
]
