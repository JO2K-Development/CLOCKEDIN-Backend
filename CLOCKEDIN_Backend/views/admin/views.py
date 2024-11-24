from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from CLOCKEDIN_Backend.models import Company, Invitation, InvitationStatus, Role, RoleEnum
from CLOCKEDIN_Backend.permissions import IsAtLeastManager
from CLOCKEDIN_Backend.serializers import InvitationSerializer
from CLOCKEDIN_Backend.utils.mailing.canceled_invitation_mail import send_cancelled_invitation_email
from CLOCKEDIN_Backend.utils.mailing.welcome_mail_sender import send_welcome_email


class InviteView(APIView):
    permission_classes = [IsAtLeastManager]

    def post(self, request):
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
        # invitation.roles.set(roles)  # Assign roles

        return JsonResponse(
            {"message": f"Invitation sent and user created! {request.user.is_authenticated}, {request.user}"},
            status=status.HTTP_200_OK,
        )

    def delete(self, request):
        # Validate company ID
        company_id = request.user.company_id
        if not company_id:
            return Response(
                {"error": "Company ID not in inviter data"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get email value
        params = request.query_params
        inv_email = params.get("email")  # Dont wheter to check if the email exists

        # Get invitation related to that email and company
        if not inv_email:
            return Response(
                {"error": "Email not provided in the parameters"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        invitation = get_object_or_404(Invitation, email=inv_email, company=company_id, status=InvitationStatus.PENDING)
        invitation.delete()

        send_cancelled_invitation_email(inv_email)

        return JsonResponse(
            {"message": f"Invitation has been cancelled! {request.user.is_authenticated}, {request.user}"},
            status=status.HTTP_200_OK,
        )
