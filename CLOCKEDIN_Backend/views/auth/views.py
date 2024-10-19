from django.db import transaction
from rest_framework import generics, status
from rest_framework.response import Response

from CLOCKEDIN_Backend.models.custom_social_account_adapter import logger
from CLOCKEDIN_Backend.models.email_adress import EmailAddress
from CLOCKEDIN_Backend.serializers.custom_register_serializer import CustomRegisterSerializer


class CustomRegisterView(generics.CreateAPIView):
    serializer_class = CustomRegisterSerializer

    @transaction.atomic  # Ensure atomicity
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save the user
        logger.info(f"Registering user {serializer.validated_data['email']}")
        user = serializer.save(request=request)
        logger.info(f"User {user.email} registered successfully")
        user.save()
        logger.info(f"User {user.email} saved successfully")

        email_address = EmailAddress.objects.create(user=user, email=user.email)

        return Response({"user": serializer.data}, status=status.HTTP_201_CREATED)
