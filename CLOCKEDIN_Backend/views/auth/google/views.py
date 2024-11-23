import requests
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from CLOCKEDIN_Backend.models import Company
from CLOCKEDIN_Backend.models.role import RoleEnum


class GoogleLogin(APIView):
    def post(self, request):
        token = request.data.get("token")
        is_admin = request.data.get("is_admin", False)
        company_name = request.data.get("company_name", None)

        # Verify the token with Google
        response = requests.get(
            f"https://oauth2.googleapis.com/tokeninfo?id_token={token}"
        )
        if response.status_code != 200:
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )

        user_info = response.json()
        email = user_info.get("email")
        User = get_user_model()

        user, created = User.objects.get_or_create(email=email)

        if is_admin:
            if not company_name:
                return Response(
                    {"error": "Company name is required for admin users"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            company = Company.objects.create(name=company_name)
            user.company = company
            user.is_staff = True
            user.roles.add(RoleEnum.ADMIN.value)
            user.roles.add(RoleEnum.MANAGER.value)
            user.roles.add(RoleEnum.EMPLOYEE.value)
            user.save()

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({"access_token": access_token}, status=status.HTTP_200_OK)
