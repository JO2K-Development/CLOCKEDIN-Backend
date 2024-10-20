from dj_rest_auth.registration.views import RegisterView
from rest_framework import status
from rest_framework.response import Response
from CLOCKEDIN_Backend.models.email_adress import EmailAddress
from CLOCKEDIN_Backend.serializers.custom_register_serializer import CustomRegisterSerializer
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save(request=request)  # Save the user
            user.save()  # Ensure the user is saved before creating related objects
            logger.debug("User saved successfully")

            # Now, create related objects like EmailAddress
            email_address = EmailAddress(user=user, email=user.email)
            email_address.save()  # Save the instance to the database
            logger.debug("EmailAddress saved successfully")

            return Response({"user": serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error occurred: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)