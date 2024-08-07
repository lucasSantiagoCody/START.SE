from django.urls import path
from . import views


urlpatterns = [
    path('register-company/', views.register_company_view, name='register_company_url'),
    path('companies/', views.companies_view, name='companies_url'),
    path('company/<int:company_id>/', views.company_view, name='company_url'),
]