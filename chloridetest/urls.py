from django.urls import path
from . import views

app_name = 'chloridetest'

urlpatterns = [
    path('', views.chloridetest_dashboard, name='chloridetest_dashboard'),
]



