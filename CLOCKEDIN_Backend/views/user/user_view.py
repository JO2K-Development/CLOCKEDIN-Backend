from rest_framework.viewsets import ReadOnlyModelViewSet

from CLOCKEDIN_Backend.models import User
from CLOCKEDIN_Backend.permissions import IsAtLeastEmployee
from CLOCKEDIN_Backend.serializers import UserSerializer


class UserViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsAtLeastEmployee]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
