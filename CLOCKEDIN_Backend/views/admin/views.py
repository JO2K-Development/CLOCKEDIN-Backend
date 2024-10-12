from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from CLOCKEDIN_Backend.models import User
from CLOCKEDIN_Backend.serializers import InviteSerializer
from CLOCKEDIN_Backend.utils.mailing.welcome_mail_sender import send_welcome_email

#@method_decorator(csrf_exempt, name='dispatch')
class InviteView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Pass the request data to the serializer
        serializer = InviteSerializer(data=request.data)

        # Check if the data is valid (according to the serializer's rules)
        if not serializer.is_valid():
            # If invalid, return the errors in the response
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # If valid, extract the validated data
        validated_data = serializer.validated_data
        email = validated_data['email']
        position = validated_data['position']
        role = validated_data['role']

        # Call the email sending function
        send_welcome_email(email)

        # add the user to the database
        user = User.objects.create_user(username=email, email=email, position=position, temporary=True)
        user.save()

        # Return a success message
        return JsonResponse({
            'message': f'This is a secured post endpoint! {request.user.is_authenticated}, {request.user}'
        }, status=status.HTTP_200_OK)
