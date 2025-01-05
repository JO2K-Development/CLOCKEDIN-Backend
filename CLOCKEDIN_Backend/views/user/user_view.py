from rest_framework.viewsets import ReadOnlyModelViewSet

from CLOCKEDIN_Backend.models import User
from CLOCKEDIN_Backend.permissions import IsEmployee
from CLOCKEDIN_Backend.serializers import UserSerializer


class UserViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsEmployee]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
