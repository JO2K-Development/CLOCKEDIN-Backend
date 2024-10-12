from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from CLOCKEDIN_Backend.utils.mailing.welcome_mail_sender import send_welcome_email


class UnsecuredView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        send_welcome_email(request)
        return JsonResponse(
            {'message': f'This is a not-secured get endpoint! {request.user.is_authenticated}, {request.user}'})

    def post(self, request):
        return JsonResponse(
            {'message': f'This is a unsecured post endpoint! {request.user.is_authenticated}, {request.user}'})


