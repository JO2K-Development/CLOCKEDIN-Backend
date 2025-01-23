from django.db import transaction
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response

from CLOCKEDIN_Backend.models import Company, Role, RoleEnum
from CLOCKEDIN_Backend.permissions import IsEmployee
from CLOCKEDIN_Backend.serializers.company_serializer import CreateCompanySerializer


class CreateCompanyView(GenericAPIView, CreateModelMixin):
    permission_classes = [IsEmployee]
    serializer_class = CreateCompanySerializer

    def perform_create(self, serializer):
        user = self.request.user
        company_name = serializer.validated_data.get("company_name")
        if user.company:
            return Response({"error": "User already has a company."}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            company = Company.objects.create(name=company_name)
            user.company = company
            user.is_admin = True
            for role in RoleEnum:
                user.roles.add(Role.objects.get(name=role.value))
            user.save()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
