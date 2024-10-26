from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from CLOCKEDIN_Backend.views.auth.google.views import GoogleLogin
from CLOCKEDIN_Backend.views.auth.views import CustomRegisterView

urlpatterns = [
    path("google/", GoogleLogin.as_view(), name="google_login"),
    path("registration/", CustomRegisterView.as_view(), name="custom_register"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
