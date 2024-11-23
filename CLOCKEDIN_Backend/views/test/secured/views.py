from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class SecuredView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return JsonResponse(
            {
                "message": f"This is a secured get endpoint! {request.user.is_authenticated}, {request.user}"
            }
        )

    def post(self, request):
        return JsonResponse(
            {
                "message": f"This is a secured post endpoint! {request.user.is_authenticated}, {request.user}"
            }
        )
