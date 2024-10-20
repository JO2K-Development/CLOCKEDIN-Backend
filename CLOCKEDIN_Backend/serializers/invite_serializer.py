from rest_framework import serializers

class InviteSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=50)
    position = serializers.CharField(required=True, max_length=50)
    roles = serializers.ListField(child=serializers.IntegerField())

