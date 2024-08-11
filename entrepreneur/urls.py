from django.urls import path
from . import views


urlpatterns = [
    path('register-company/', views.register_company_view, name='register_company_url'),
    path('companies/', views.companies_view, name='companies_url'),
    path('company-details/<int:company_id>/', views.company_details_view, name='entrepreneur_company_details_url'),
    path('add-document/<int:company_id>/', views.add_document_view, name='add_document_url'),
    path('delete-document/<int:document_id>/', views.delete_document_view, name='delete_document_url'),
    path('add-metric/<int:company_id>/', views.add_metric_view, name='add_metric_url'),
    path('manage-proposal/<int:id>', views.manage_proposal_view, name="manage_proposal_url")
]