from rest_framework import serializers
from CLOCKEDIN_Backend.models import User
from .role_serializer import RoleSerializer

class UserSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'position', 'roles', 'company_id']