"""
URL configuration for the authentication app API endpoints.
Maps registration and login requests to their respective views.
"""

from django.urls import path
from auth_app.api.views import CustomLoginView, RegistrationView


urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', CustomLoginView.as_view(), name='login'),
]