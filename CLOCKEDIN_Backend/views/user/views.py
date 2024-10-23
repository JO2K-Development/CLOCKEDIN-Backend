import logging

import jwt
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from CLOCKEDIN_Backend.models.company import Company
from CLOCKEDIN_Backend.models.invitation import Invitation
from CLOCKEDIN_Backend.serializers.user_serializer import UserSerializer

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class InvitationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_email = request.user.email
        invitations = Invitation.objects.filter(email=user_email, status='pending')

        if not invitations.exists():
            return Response({"error": "No pending invitations found"}, status=status.HTTP_404_NOT_FOUND)

        invitation_data = [
            {"id": inv.id, "email": inv.email, "company_id": inv.company.id, "company_name": inv.company.name}
            for inv in invitations
        ]
        return Response({"invitations": invitation_data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user
        invitation_id = request.data.get('invitation_id')

        if not invitation_id:
            return Response({"error": "Invitation ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            invitation = Invitation.objects.get(id=invitation_id)
        except Invitation.DoesNotExist:
            return Response({"error": "Invitation not found"}, status=status.HTTP_404_NOT_FOUND)

        if invitation.email != user.email:
            return Response({"error": "Invitation does not belong to this user"}, status=status.HTTP_400_BAD_REQUEST)

        if invitation.status != 'pending':
            return Response({"error": "Invitation has already been accepted or rejected"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            company = Company.objects.get(id=invitation.company_id)
        except Company.DoesNotExist:
            return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)

        # Accept the invitation and link the user to the company
        invitation.status = 'accepted'
        invitation.save()
        user.company = company
        user.position = invitation.position
        user.roles.set(invitation.roles.all())
        user.save()

        logger.debug(f"User {user.email} joined company: {company.name}")
        return Response({"message": "Company joined successfully"}, status=status.HTTP_200_OK)


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
