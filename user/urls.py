from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup_url'),
    path('login/', views.login_view, name='login_url'),
]