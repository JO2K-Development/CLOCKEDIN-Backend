from rest_framework import serializers

class InviteSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=50)
    position = serializers.CharField(required=True, max_length=50)
    role = serializers.CharField(required=True, max_length=50)
