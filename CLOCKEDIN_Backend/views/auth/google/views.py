import requests
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from CLOCKEDIN_Backend.models import Company
from CLOCKEDIN_Backend.models.role import Role, RoleEnum


class GoogleLogin(APIView):
    authentication_classes = [AllowAny]

    def post(self, request):
        token = request.data.get("token")

        # Verify the token with Google
        response = requests.get(f"https://oauth2.googleapis.com/tokeninfo?id_token={token}")
        if response.status_code != 200:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

        user_info = response.json()
        email = user_info.get("email")
        User = get_user_model()

        user, created = User.objects.get_or_create(email=email)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({"access_token": access_token}, status=status.HTTP_200_OK)
