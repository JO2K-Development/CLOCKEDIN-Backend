from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from CLOCKEDIN_Backend.models import Company, Invitation, User, Role
from CLOCKEDIN_Backend.models.role import RoleEnum
from CLOCKEDIN_Backend.permissions import IsAdmin, IsManager
from CLOCKEDIN_Backend.serializers import InvitationSerializer
from CLOCKEDIN_Backend.utils.mailing.canceled_invitation_mail import (
    send_cancelled_invitation_email,
)
from CLOCKEDIN_Backend.utils.mailing.welcome_mail_sender import send_welcome_email


class InviteView(APIView):
    permission_classes = [IsAdmin, IsManager]

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
        roles = validated_data["roles"]

        # Send welcome email (assumed to be a side effect)
        send_welcome_email(email)

        # Use get_object_or_404 for company lookup
        company = get_object_or_404(Company, id=company_id)

        # Create and save the invitation
        invitation = Invitation(email=email, company=company, position=position)
        invitation.save()
        invitation.roles.set(roles)  # Assign roles

        return JsonResponse(
            {
                "message": f"Invitation sent and user created! {request.user.is_authenticated}, {request.user}"
            },
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

        invitation = get_object_or_404(
            Invitation, email=inv_email, company=company_id, status="pending"
        )
        invitation.delete()

        send_cancelled_invitation_email(inv_email)

        return JsonResponse(
            {
                "message": f"Invitation has been cancelled! {request.user.is_authenticated}, {request.user}"
            },
            status=status.HTTP_200_OK,
        )


class RemoveEmployeeView(APIView):
    permission_classes = [IsAdmin, IsManager]

    def patch(self, request):
        """unset the company_id of the user"""
        company_id = request.user.company_id
        if not company_id:
            return JsonResponse({"error": "User is not assigned to any company"}, status=status.HTTP_400_BAD_REQUEST)

        user_id = request.data.get("user_id", None)
        if user_id is None:
            return JsonResponse({"error": "user_id not provided"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=user_id)
        user.company_id=None
        user.roles.clear()
        user.save()
        return JsonResponse({"message": "User removed from company"}, status=status.HTTP_200_OK)


class EmployeeRolesView(APIView):
    permission_classes = [IsAdmin, IsManager]

    def patch(self, request):
        """change user roles"""
        company_id = request.user.company_id
        if not company_id:
            return JsonResponse({"error": "User is not assigned to any company"}, status=status.HTTP_400_BAD_REQUEST)
        
        user_id = request.data.get("user_id", None)
        if user_id is None:
            return JsonResponse({"error": "Id not provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        body = request.data
        if "new_role" in body:
            allowed_roles = [RoleEnum.MANAGER.name, RoleEnum.EMPLOYEE.name]
            if body["new_role"] not in allowed_roles:
                return JsonResponse({"error": "Incorrect"}, status=status.HTTP_400_BAD_REQUEST)
            user = get_object_or_404(User, id=user_id)
            role = get_object_or_404(Role, name=body["new_role"])
            user.role = role
            user.save()
            return JsonResponse({"message": "User role changed"}, status=status.HTTP_200_OK)
        
class EmployeePositionView(APIView):
    def patch(self, request):
        """change user roles"""
        company_id = request.user.company_id
        if not company_id:
            return JsonResponse({"error": "User is not assigned to any company"}, status=status.HTTP_400_BAD_REQUEST)
        
        user_id = request.data.get("user_id", None)
        if user_id is None:
            return JsonResponse({"error": "Id not provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        body = request.data
        if "position" in body:
            user = get_object_or_404(User, id=user_id)
            user.position = request.data["position"]  
            user.save()         
            return JsonResponse({"message": "User position changed"}, status=status.HTTP_200_OK)
        