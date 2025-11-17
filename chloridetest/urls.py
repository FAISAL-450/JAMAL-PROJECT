from django.urls import path
from . import views

urlpatterns = [
    path('', views.ctr_dashboard, name='ctr_dashboard'),
]

