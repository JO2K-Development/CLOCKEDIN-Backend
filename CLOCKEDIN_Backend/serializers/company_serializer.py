from rest_framework import serializers

from CLOCKEDIN_Backend.models import Company


class CreateCompanySerializer(serializers.ModelSerializer):
    company_name = serializers.CharField()

    class Meta:
        model = Company
        fields = ["company_name", "company_logo_url"]


class CompanySerializer(serializers.ModelSerializer):
    company_name = serializers.CharField()

    class Meta:
        model = Company
        fields = ["company_name", "company_logo_url"]