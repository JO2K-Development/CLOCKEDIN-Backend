import logging

import jwt
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from CLOCKEDIN_Backend.models import User
from CLOCKEDIN_Backend.models.company import Company
from CLOCKEDIN_Backend.models.invitation import Invitation

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ChooseCompanyView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return Response({"error": "Authorization header missing"}, status=status.HTTP_401_UNAUTHORIZED)

            token = auth_header.split(' ')[1]
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = decoded_token.get('user_id')
            user_email = User.objects.get(id=user_id).email

            # Find current invitations for the user
            invitations = Invitation.objects.filter(email=user_email, status='pending')

            if not invitations.exists():
                return Response({"error": "No pending invitations found"}, status=status.HTTP_404_NOT_FOUND)

            # Process the invitations as needed
            invitation_data = [{"id": inv.id, "email": inv.email, "company": inv.company.name} for inv in invitations]

            return Response({"invitations": invitation_data}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error occurred: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def post(self, request, *args, **kwargs):
        try:
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return Response({"error": "Authorization header missing"}, status=status.HTTP_401_UNAUTHORIZED)

            token = auth_header.split(' ')[1]
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = decoded_token.get('user_id')
            user = User.objects.get(id=user_id)
            company_id = request.data.get('company_id')
            if not company_id:
                return Response({"error": "Company ID is required"}, status=status.HTTP_400_BAD_REQUEST)

            company = Company.objects.get(id=company_id)

            invitation = Invitation.objects.filter(company_id=company.id , status='pending').first()
            if not invitation:
                return Response({"error": "No pending invitation found for this company"}, status=status.HTTP_400_BAD_REQUEST)

            # Accept the invitation and link the user to the company
            invitation.status = 'accepted'
            invitation.save()
            user.company = company
            user.save()
            logger.debug(f"User {user.email} joined company: {company.name}")

            return Response({"message": "Company joined successfully"}, status=status.HTTP_200_OK)
        except Company.DoesNotExist:
            return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error occurred: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)