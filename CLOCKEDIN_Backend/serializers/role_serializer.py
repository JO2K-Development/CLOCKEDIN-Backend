from rest_framework import serializers

from CLOCKEDIN_Backend.models.role import Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']