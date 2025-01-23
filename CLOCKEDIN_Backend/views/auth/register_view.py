import logging

from dj_rest_auth.registration.views import RegisterView
from django.db import IntegrityError, transaction
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from CLOCKEDIN_Backend.models import Company, Role, RoleEnum, User
from CLOCKEDIN_Backend.serializers import CustomRegisterSerializer

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class CustomRegisterView(RegisterView):
    permission_classes = [AllowAny]
    serializer_class = CustomRegisterSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        # Fetch the user data directly using the email from the request
        email = request.data.get("email")
        if not email:
            return Response(
                {"error": "Email not provided in request data."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "User with this email already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Call the parent class's create method to handle user creation and email sending
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(email=email)
        user.roles.add(Role.objects.get(name=RoleEnum.Employee.value))
        user.save()

        return response
