from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from CLOCKEDIN_Backend.models import Company, Invitation, InvitationStatus, Role, RoleEnum
from CLOCKEDIN_Backend.permissions import IsAtLeastManager
from CLOCKEDIN_Backend.serializers import InvitationSerializer
from CLOCKEDIN_Backend.utils.mailing import send_cancelled_invitation_email, send_welcome_email

class InvitationViewSet(ViewSet):
    permission_classes = [IsAtLeastManager]

    def create(self, request):
        # Validate company ID
        company_id = request.user.company_id
        if not company_id:
            return Response(
                {"error": "Company ID not in inviter data"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate input data
        serializer = InvitationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Get validated data
        validated_data = serializer.validated_data
        email = validated_data["email"]
        position = validated_data["position"]
        role = validated_data["role"]

        if role in RoleEnum.__members__:
            role = Role.objects.get(id=RoleEnum[role].value)
        else:
            role = Role.objects.get(id=RoleEnum.Employee.value)

        send_welcome_email(email)

        company = get_object_or_404(Company, id=company_id)

        # Create and save the invitation
        invitation = Invitation(email=email, company=company, position=position, role=role)
        invitation.save()

        return Response(
            {"message": "Invitation sent and user created!"},
            status=status.HTTP_201_CREATED,
        )

    @action(detail=False, methods=['delete'], url_path='cancel')
    def cancel(self, request):
        # Validate company ID
        company_id = request.user.company_id
        if not company_id:
            return Response(
                {"error": "Company ID not in inviter data"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get email value
        inv_email = request.query_params.get("email")
        if not inv_email:
            return Response(
                {"error": "Email not provided in the parameters"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get invitation related to that email and company
        invitation = get_object_or_404(
            Invitation,
            email=inv_email,
            company=company_id,
            status=InvitationStatus.PENDING
        )
        invitation.delete()

        send_cancelled_invitation_email(inv_email)

        return Response(
            {"message": "Invitation has been cancelled!"},
            status=status.HTTP_200_OK,
        )
