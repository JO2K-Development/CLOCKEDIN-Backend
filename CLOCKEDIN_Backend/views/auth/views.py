import logging

from dj_rest_auth.registration.views import RegisterView
from django.db import IntegrityError, transaction
from rest_framework import status
from rest_framework.response import Response

from CLOCKEDIN_Backend.models.company import Company
from CLOCKEDIN_Backend.models.role import RoleEnum
from CLOCKEDIN_Backend.models.user import User
from CLOCKEDIN_Backend.serializers.custom_register_serializer import (
    CustomRegisterSerializer,
)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        # Call the parent class's create method to handle user creation and email sending
        response = super().create(request, *args, **kwargs)

        # Fetch the user data directly using the email from the request
        email = request.data.get("email")
        if not email:
            return Response(
                {"error": "Email not provided in request data."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

        # Check if the user is an admin and create a company
        if request.data.get("is_admin", False):
            company_name = request.data.get("company_name")
            if not company_name:
                logger.warning("Admin registration requires a company name")
                return Response(
                    {"error": "Company name is required for admin registration"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Now wrap only the DB operation in a try-catch
            try:
                # Creating the company and associating it with the user
                company = Company.objects.create(name=company_name)
                user.company = company
                user.is_admin = True
                user.roles.add(RoleEnum.Admin.value)
                user.roles.add(RoleEnum.Manager.value)
                user.roles.add(RoleEnum.Employee.value)
                user.save()
                logger.debug(f"Admin user {user.email} created company: {company.name}")

            except IntegrityError as e:
                logger.error(f"Integrity error while creating company: {e}")
                transaction.set_rollback(True)  # Rollback any partial database changes
                return Response(
                    {"error": "Database error occurred while creating company."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            except Exception as e:
                logger.error(f"Unexpected error while creating company: {e}")
                return Response(
                    {"error": "An unexpected error occurred. Please try again."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return response
