from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from CLOCKEDIN_Backend.models import User
from CLOCKEDIN_Backend.permissions import IsManager
from CLOCKEDIN_Backend.serializers import UserSerializer


class ManageEmployeesView(ViewSet):
    permission_classes = [IsManager]

    def get_queryset(self, request):
        return User.objects.filter(company=request.user.company)

    @action(detail=False, methods=['get'], url_path='without-manager')
    def get_users_without_manager(self, request):
        users_without_manager = self.get_queryset(request).filter(manager__isnull=True)
        serializer = UserSerializer(users_without_manager, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='assign-user')
    def assign_user_to_manager(self, request):
        user_id = request.data.get('user_id')
        user = self.get_queryset(request).filter(id=user_id, manager__isnull=True).first()
        if user:
            user.manager = request.user
            user.save()
            return Response({"detail": "User assigned to manager successfully."}, status=status.HTTP_200_OK)
        return Response({"detail": "User not found or already assigned to a manager."},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='detach-user')
    def detach_user_from_manager(self, request):
        user_id = request.data.get('user_id')
        user = self.get_queryset(request).filter(id=user_id, manager=request.user).first()
        if user:
            user.manager = None
            user.save()
            return Response({"detail": "User detached from manager successfully."}, status=status.HTTP_200_OK)
        return Response({"detail": "User not found or not assigned to this manager."},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='assigned-users')
    def get_assigned_users(self, request):
        assigned_users = self.get_queryset(request).filter(manager=request.user)
        serializer = UserSerializer(assigned_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
