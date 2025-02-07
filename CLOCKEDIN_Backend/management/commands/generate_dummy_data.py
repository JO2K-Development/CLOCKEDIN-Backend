from django.core.management.base import BaseCommand
from django.db import transaction

from CLOCKEDIN_Backend.models import User, Company


class Command(BaseCommand):
    help = 'Generate dummy data for the database'

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            User.objects.create_superuser(
                first_name="user",
                email="user@example.com",
                password="password"
            )

            # Create dummy users
            users = [User(first_name=f"user{i}", email=f"email@usr{i}.com") for i in range(1, 40)]
            User.objects.bulk_create(users)

            # Create dummy companies
            companies = [Company(name=f"Company{i}") for i in range(1, 6)]
            Company.objects.bulk_create(companies)

            # Link users to companies
            for i in range(1, 40):
                user = User.objects.get(first_name=f"user{i}")
                company = Company.objects.get(name=f"Company{i % 5 + 1}")
                user.company = company
                user.save()
