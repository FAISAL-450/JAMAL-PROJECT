from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.proposal_dashboard, name='proposal_dashboard'),
    path('dashboard/<int:proposal_id>/', views.proposal_dashboard, name='proposal_dashboard'),
    path('create/', views.create_proposal, name='create_proposal'),
    path('<int:proposal_id>/upload/', views.upload_documents, name='upload_documents'),
    path('<int:proposal_id>/send/', views.send_proposal_email, name='send_proposal_email'),
]
