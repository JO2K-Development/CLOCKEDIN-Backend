from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from CLOCKEDIN_Backend.models import Company, Invitation, User, Role
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

        User.objects.get(id=user_id).update(company_id=None)
        return JsonResponse({"message": "User removed from company"}, status=status.HTTP_200_OK)


class CompanyEmployeeStatusView(APIView):
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
        if "role" in body:            
            # TODO: handles current version of app (three basic roles),
            # doesn't handle multiple roles assignment
            acceptable = ["Manager", "Employee"]
            new_role = request.data["role"]
            if new_role not in acceptable:
                return JsonResponse({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)
            
            
            new_role_id = Role.objects.get(role=new_role).id
            get_object_or_404(Role, user_id=user_id).update(role_id=new_role_id)
            return JsonResponse({"message": "User role changed"}, status=status.HTTP_200_OK)
        
        
        if "position" in body:
            get_object_or_404(User, id=user_id).update(position=request.data["position"])
            return JsonResponse({"message": "User position changed"}, status=status.HTTP_200_OK)
        
