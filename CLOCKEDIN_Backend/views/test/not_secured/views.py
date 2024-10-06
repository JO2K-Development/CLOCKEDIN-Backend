from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView


class NotSecuredView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return JsonResponse(
            {'message': f'This is a not-secured get endpoint! {request.user.is_authenticated}, {request.user}'})

    def post(self, request):
        return JsonResponse(
            {'message': f'This is a unsecured post endpoint! {request.user.is_authenticated}, {request.user}'})


