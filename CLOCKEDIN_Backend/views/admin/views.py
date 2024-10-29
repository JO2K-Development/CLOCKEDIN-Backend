from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from CLOCKEDIN_Backend.models import Company, Invitation, User
from CLOCKEDIN_Backend.permissions import IsAdmin, IsManager
from CLOCKEDIN_Backend.serializers import InviteSerializer
from CLOCKEDIN_Backend.utils.mailing.welcome_mail_sender import send_welcome_email


class InviteView(APIView):
    permission_classes = [IsAdmin, IsManager]

    def post(self, request):
        # Validate company ID
        company_id = request.user.company_id
        if not company_id:
            return Response({"error": "Company ID not in inviter data"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate input data
        serializer = InviteSerializer(data=request.data)
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
            {"message": f"Invitation sent and user created! {request.user.is_authenticated}, {request.user}"},
            status=status.HTTP_200_OK,
        )


class EmployeesManagmentView(APIView):
    permission_classes = [IsAdmin, IsManager]

    def patch(self, request):
        """unset the company_id of the user"""
        company_id = request.user.company_id
        if not company_id:
            return JsonResponse({"error": "User is not assigned to any company"}, status=status.HTTP_400_BAD_REQUEST)

        email = request.data.get("email", None)
        if email is None:
            return JsonResponse({"error": "Email not provided"}, status=status.HTTP_400_BAD_REQUEST)

        User.objects.filter(email=email).update(company_id=None)
        return JsonResponse({"message": "User removed from company"}, status=status.HTTP_200_OK)

    def patch(self, request):
        """change user roles"""
        company_id = request.user.company_id
        if not company_id:
            return JsonResponse({"error": "User is not assigned to any company"}, status=status.HTTP_400_BAD_REQUEST)
        # TODO: handles current version of app (three basic roles),
        # doesn't handle multiple roles assignment
        acceptable = ["Manager", "Employee"]
        new_role = request.data.get("role", None)
        if new_role not in acceptable:
            return JsonResponse({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)
        get_object_or_404(User, request.data["email"]).update(role=new_role)
        return JsonResponse({"message": "User role changed"}, status=status.HTTP_200_OK)
