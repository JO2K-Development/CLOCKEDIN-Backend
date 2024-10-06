from django.urls import path

from CLOCKEDIN_Backend.views.login.google.views import GoogleLogin

urlpatterns = [
    path('google/', GoogleLogin.as_view(), name='google_login'),
]