import logging

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from CLOCKEDIN_Backend.models import User
from CLOCKEDIN_Backend.models.company import Company
from CLOCKEDIN_Backend.models.invitation import Invitation
from CLOCKEDIN_Backend.serializers import InvitationSerializer
from CLOCKEDIN_Backend.serializers.invite_serializer import AcceptInvitationSerializer
from CLOCKEDIN_Backend.serializers.user_serializer import UserSerializer

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class InvitationViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InvitationSerializer
    queryset = Invitation.objects.filter(status="pending")

    def get_queryset(self):
        # Filter invitations to only those that belong to the authenticated user
        return self.queryset.filter(email=self.request.user.email)

    @action(detail=False, methods=["post"], url_path="accept", serializer_class=AcceptInvitationSerializer)
    def accept(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        invitation_id = serializer.validated_data.get("invitation_id")

        try:
            invitation = Invitation.objects.get(id=invitation_id, email=request.user.email)
        except Invitation.DoesNotExist:
            return Response(
                {"error": "Invitation not found or does not belong to this user"}, status=status.HTTP_404_NOT_FOUND
            )

        if invitation.status != "pending":
            return Response(
                {"error": "Invitation has already been accepted or rejected"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            company = Company.objects.get(id=invitation.company_id)
        except Company.DoesNotExist:
            return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)

        # Accept the invitation and link the user to the company
        invitation.status = "accepted"
        invitation.save()
        request.user.company = company
        request.user.position = invitation.position
        request.user.roles.set(invitation.roles.all())
        request.user.save()

        return Response({"message": "Company joined successfully"}, status=status.HTTP_200_OK)


from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet


class UserViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
