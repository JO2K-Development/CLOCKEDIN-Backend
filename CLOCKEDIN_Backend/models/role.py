from enum import Enum

from django.db import models


class RoleEnum(Enum):
    Admin = "admin"
    Manager = "manager"
    Employee = "employee"


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True, default='Employee')

    def __str__(self):
        return self.name
