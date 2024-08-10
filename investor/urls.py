from django.urls import path
from . import views


urlpatterns = [
    path('suggestion/', views.suggestion_view, name='suggestion_url'),
    path('company-details/<int:company_id>/', views.company_details_view, name='company_details_url'),
    path('make-proposal/<int:company_id>', views.make_proposal_view, name="make_proposal_url"),
]