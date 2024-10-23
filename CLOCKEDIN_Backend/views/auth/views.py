from dj_rest_auth.registration.views import RegisterView
from rest_framework import status
from rest_framework.response import Response
from CLOCKEDIN_Backend.models.company import Company
from CLOCKEDIN_Backend.serializers.custom_register_serializer import CustomRegisterSerializer
from django.db import transaction, IntegrityError
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        # Validation and user creation don't need try-catch here
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Validation errors handled automatically
        user = serializer.save(request=request)
        user.save()
        logger.debug(f"User {user.email} saved successfully")

        # Check if the user is an admin and create a company
        if request.data.get('is_admin', False):
            company_name = request.data.get('company_name')
            if not company_name:
                logger.warning("Admin registration requires a company name")
                return Response({"error": "Company name is required for admin registration"},
                                status=status.HTTP_400_BAD_REQUEST)

            # Now wrap only the DB operation in a try-catch
            try:
                # Creating the company and associating it with the user
                company = Company.objects.create(name=company_name)
                user.company = company
                user.is_admin = True
                user.save()
                logger.debug(f"Admin user {user.email} created company: {company.name}")

            except IntegrityError as e:
                logger.error(f"Integrity error while creating company: {e}")
                transaction.set_rollback(True)  # Rollback any partial database changes
                return Response({"error": "Database error occurred while creating company."},
                                status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                logger.error(f"Unexpected error while creating company: {e}")
                return Response({"error": "An unexpected error occurred. Please try again."},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"user": serializer.data}, status=status.HTTP_201_CREATED)
