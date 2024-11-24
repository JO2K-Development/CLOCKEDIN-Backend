from rest_framework import serializers

from CLOCKEDIN_Backend.models import Invitation


class InvitationSerializer(serializers.ModelSerializer):
    company_id = serializers.IntegerField(source="company.id")
    company_name = serializers.CharField(source="company.name")

    class Meta:
        model = Invitation
        fields = ["id", "email", "position", "role"]


class AcceptInvitationSerializer(serializers.Serializer):
    invitation_id = serializers.IntegerField()


class AcceptInvitationResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
