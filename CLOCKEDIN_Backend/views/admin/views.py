import jwt
from django.conf import settings
from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from CLOCKEDIN_Backend.models import User, Company, Invitation
from CLOCKEDIN_Backend.serializers import InviteSerializer
from CLOCKEDIN_Backend.utils.mailing.welcome_mail_sender import send_welcome_email

class InviteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Decode the token to get the company_id
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return Response({"error": "Authorization header missing"}, status=status.HTTP_401_UNAUTHORIZED)

        token = auth_header.split(' ')[1]
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = decoded_token.get('user_id')
        company_id = User.objects.get(id=user_id).company_id

        if not company_id:
            return Response({"error": "Company ID not found in token"}, status=status.HTTP_400_BAD_REQUEST)

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

        # Create the invitation object
        try:
            company = Company.objects.get(id=company_id)
            invitation = Invitation.objects.create(email=email, company=company)
            invitation.save()
        except Company.DoesNotExist:
            return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)


        # Return a success message
        return JsonResponse({
            'message': f'Invitation sent and user created! {request.user.is_authenticated}, {request.user}'
        }, status=status.HTTP_200_OK)