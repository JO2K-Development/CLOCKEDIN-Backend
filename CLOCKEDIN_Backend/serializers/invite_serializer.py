from rest_framework import serializers

from CLOCKEDIN_Backend.models import Invitation


class InviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ["id", "email", "position", "roles"]
