import requests
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

class GoogleLogin(APIView):
    def post(self, request):
        token = request.data.get('token')  # User's Google OAuth token
        if not token:
            return Response({'error': 'Token not provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Verify the token with Google
        response = requests.get(f'https://oauth2.googleapis.com/tokeninfo?id_token={token}')
        if response.status_code != 200:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        user_info = response.json()
        email = user_info.get('email')

        # Get or create the user
        User = get_user_model()
        user, created = User.objects.get_or_create(email=email)

        # Generate or retrieve token
        token, _ = Token.objects.get_or_create(user=user)

        # Return the token to the user
        return Response({'token': token.key}, status=status.HTTP_200_OK)