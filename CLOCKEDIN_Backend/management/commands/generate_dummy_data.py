import os
from django.core.management.base import BaseCommand
from django.db import transaction
from django.core.management import call_command

from CLOCKEDIN_Backend.models import User, Company, Invitation


class Command(BaseCommand):
    help = 'Generate dummy data for the database'

    def add_arguments(self, parser):
        parser.add_argument('--force', action="store_true", help='Force overwrite the database')

    def handle(self, *args, **kwargs):
        if os.path.exists('db.sqlite3'):
            if kwargs['force']:
                os.remove('db.sqlite3')
            else:
                print("Database already exists. Use 'force' argument to overwrite it.")
                return
        call_command('makemigrations')
        call_command('migrate')
        
        
        SUPER_USER_EMAIL = "user@example.com"
        dummy_positions = ["Developer", "Project Manager", "Designer", "Tester", "HR", "Finance", "Marketing", "Sales"]
        COMPANY_COUNT = 5
        USERS_COUNT = 40
        if USERS_COUNT < COMPANY_COUNT:
            raise ValueError("Number of users must be greater than number of companies")
        
        with transaction.atomic():
            User.objects.create_superuser(
                first_name="user",
                last_name="lastname",
                email=SUPER_USER_EMAIL,
                password="password"
            )
            # Create dummy users
            users = [User(first_name=f"user{i}", last_name="Lastname", email=f"email@usr{i}.com") for i in range(1, USERS_COUNT + 1)]
            User.objects.bulk_create(users)

            # Create dummy companies
            companies = []
            for i in range(1, COMPANY_COUNT + 1):
                owner = User.objects.get(email=f"email@usr{i}.com")
                owner.first_name = f"owner{i}"
                owner.save()
                companies.append(Company(name=f"Company{i}", owner=owner))
                
            Company.objects.bulk_create(companies)

            # Link users to companies
            for i in range(COMPANY_COUNT + 1, USERS_COUNT + 1):
                user = User.objects.get(first_name=f"user{i}")
                company = Company.objects.get(name=f"Company{i % COMPANY_COUNT + 1}")
                user.company = company
                user.position = dummy_positions[i % len(dummy_positions)]
                user.save()
                
            # Make dummy invitations for the superuser
            superuser = User.objects.get(email=SUPER_USER_EMAIL)
            
            for i in range(1,4):
                company = Company.objects.get(name=f"Company{i}")
                Invitation.objects.create(
                    email=superuser.email,
                    company=company,
                    # say the owner is always doing the inviting
                    # inviter=company.owner,
                    position=dummy_positions[i % len(dummy_positions)],
                )