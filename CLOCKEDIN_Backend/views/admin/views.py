from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from CLOCKEDIN_Backend.models import Company, Invitation
from CLOCKEDIN_Backend.serializers import InviteSerializer
from CLOCKEDIN_Backend.utils.mailing.welcome_mail_sender import send_welcome_email


class InviteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        company_id = request.user.company_id

        if not company_id:
            return Response({"error": "Company ID not in inviter data"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = InviteSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        email = validated_data['email']
        position = validated_data['position']
        roles = validated_data['roles']

        send_welcome_email(email)

        try:
            company = Company.objects.get(id=company_id)
            invitation = Invitation(email=email, company=company, position=position)
            invitation.save()
            invitation.roles.set(roles)  # Use set() to assign roles
        except Company.DoesNotExist:
            return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)

        return JsonResponse({
            'message': f'Invitation sent and user created! {request.user.is_authenticated}, {request.user}'
        }, status=status.HTTP_200_OK)