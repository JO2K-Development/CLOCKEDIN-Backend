from rest_framework import serializers

from CLOCKEDIN_Backend.models import User
from CLOCKEDIN_Backend.serializers import RoleSerializer


class UserSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "position",
            "image_url",
            "roles",
            "company_id",
            "manager_id",
        ]


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "image_url"]
