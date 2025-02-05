from rest_framework.generics import RetrieveUpdateAPIView

from CLOCKEDIN_Backend.permissions import IsEmployee
from CLOCKEDIN_Backend.serializers import UserSerializer, UserUpdateSerializer


class UserView(RetrieveUpdateAPIView):
    permission_classes = [IsEmployee]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method == "PATCH" or self.request.method == "PUT":
            return UserUpdateSerializer
        return UserSerializer
