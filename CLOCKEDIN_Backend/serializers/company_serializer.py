from rest_auth.app_settings import serializers


class CreateCompanySerializer(serializers.ModelSerializer):
    company_name = serializers.CharField()

    class Meta:
        model = serializers.get_user_model()
        fields = ["company_name"]
