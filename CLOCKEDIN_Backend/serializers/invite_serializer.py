from rest_framework import serializers

from CLOCKEDIN_Backend.models import Invitation


class InvitationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Invitation
        fields = ["email", "position", "roles"]

    def get_roles(self, obj):
        return [role.name for role in obj.roles.all()]


class InvitationInfoSerializer(serializers.ModelSerializer):
    company_id = serializers.IntegerField(source="company.id")
    company_name = serializers.CharField(source="company.name")
    company_logo_url = serializers.CharField(source="company.company_logo_url")

    class Meta:
        model = Invitation
        fields = ["company_id", "company_name", "company_logo_url", "id", "email", "position", "roles"]

    def get_roles(self, obj):
        return [role.name for role in obj.roles.all()]


class AcceptInvitationSerializer(serializers.Serializer):
    invitation_id = serializers.IntegerField()


class AcceptInvitationResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
