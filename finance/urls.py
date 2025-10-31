from django.urls import path
from . import views
app_name = 'finance'
urlpatterns = [
    path('account-details/', views.finance_ac_list, name='finance_ac_list'),
    
]
