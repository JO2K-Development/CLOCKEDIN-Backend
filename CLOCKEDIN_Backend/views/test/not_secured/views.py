from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import status

class UnsecuredView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            return JsonResponse(
                {'message': f'This is a not-secured get endpoint! {request.user.is_authenticated}, {request.user}'})
        except APIException as e:
            return Response({'error': str(e)}, status=e.status_code)
        except Exception as e:
            return Response({'error': 'An unexpected error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            return JsonResponse(
                {'message': f'This is a unsecured post endpoint! {request.user.is_authenticated}, {request.user}'})
        except APIException as e:
            return Response({'error': str(e)}, status=e.status_code)
        except Exception as e:
            return Response({'error': 'An unexpected error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)