from django.urls import path
from . import views


urlpatterns = [
    path('register-company/', views.register_company_view, name='register_company_url'),
    path('companies/', views.companies_view, name='companies_url'),
    path('company/<int:company_id>/', views.company_view, name='company_url'),
    path('add_document/<int:company_id>/', views.add_document_view, name='add_document_url'),

]