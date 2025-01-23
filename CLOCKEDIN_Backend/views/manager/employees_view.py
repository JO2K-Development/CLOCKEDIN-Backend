from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from CLOCKEDIN_Backend.models import User
from CLOCKEDIN_Backend.permissions import IsManager
from CLOCKEDIN_Backend.serializers import UserSerializer


class UsersWithoutManagerView(ListAPIView):
    permission_classes = [IsManager]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(company=self.request.user.company, manager__isnull=True)


class AssignUserToManagerView(APIView):
    permission_classes = [IsManager]

    def get_queryset(self):
        return User.objects.filter(company=self.request.user.company, manager__isnull=True)

    def patch(self, request, *args, **kwargs):
        user_id = kwargs.get("id")
        user = self.get_queryset().filter(id=user_id).first()
        if user:
            user.manager = request.user
            user.save()
            return Response({"message": "User assigned to manager successfully."}, status=status.HTTP_200_OK)
        return Response(
            {"error": "User not found or already assigned to a manager."}, status=status.HTTP_400_BAD_REQUEST
        )


class DetachUserFromManagerView(APIView):
    permission_classes = [IsManager]

    def get_queryset(self):
        return User.objects.filter(company=self.request.user.company, manager=self.request.user)

    def patch(self, request, *args, **kwargs):
        user_id = kwargs.get("id")
        user = self.get_queryset().filter(id=user_id).first()
        if user:
            user.manager = None  # Detach the manager
            user.save()
            return Response({"message": "User detached from manager successfully."}, status=status.HTTP_200_OK)

        return Response(
            {"error": "User not found or not assigned to this manager."}, status=status.HTTP_400_BAD_REQUEST
        )


class AssignedUsersView(ListAPIView):
    permission_classes = [IsManager]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(company=self.request.user.company, manager=self.request.user)
