import logging

import jwt
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from CLOCKEDIN_Backend.models import User
from CLOCKEDIN_Backend.models.company import Company
from CLOCKEDIN_Backend.models.invitation import Invitation
from CLOCKEDIN_Backend.serializers.user_serializer import UserSerializer

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class InvitationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            user_email = request.user.email

            # Find current invitations for the user
            invitations = Invitation.objects.filter(email=user_email, status='pending')

            if not invitations.exists():
                return Response({"error": "No pending invitations found"}, status=status.HTTP_404_NOT_FOUND)

            # Process the invitations as needed
            invitation_data = [{"id": inv.id, "email": inv.email, "company_id": inv.company.id, "company_name": inv.company.name} for inv in invitations]

            return Response({"invitations": invitation_data}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error occurred: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            invitation_id = request.data.get('invitation_id')

            if not invitation_id:
                return Response({"error": "Invitation ID is required"}, status=status.HTTP_400_BAD_REQUEST)

            invitation = Invitation.objects.get(id=invitation_id)

            if invitation.email != user.email:
                return Response({"error": "Invitation does not belong to this user"}, status=status.HTTP_400_BAD_REQUEST)

            company_id = invitation.company_id
            roles = invitation.roles.all()
            position = invitation.position

            if not company_id:
                return Response({"error": "Company ID is required"}, status=status.HTTP_400_BAD_REQUEST)

            company = Company.objects.get(id=company_id)

            if invitation.status != 'pending':
                return Response({"error": "Invitation has already been accepted or rejected"}, status=status.HTTP_400_BAD_REQUEST)

            # Accept the invitation and link the user to the company
            invitation.status = 'accepted'
            invitation.save()
            user.company = company
            user.position = position
            user.roles.set(roles)
            user.save()
            logger.debug(f"User {user.email} joined company: {company.name}")

            return Response({"message": "Company joined successfully"}, status=status.HTTP_200_OK)
        except Company.DoesNotExist:
            return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error occurred: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            # Serialize the user data
            serializer = UserSerializer(request.user)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        except jwt.ExpiredSignatureError:
            return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)

        except jwt.InvalidTokenError:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            logger.error(f"Error occurred: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
