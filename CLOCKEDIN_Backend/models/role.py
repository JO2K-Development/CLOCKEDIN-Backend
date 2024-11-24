from enum import Enum

from django.db import models


class RoleEnum(Enum):
    Admin = 1
    Manager = 2
    Employee = 3


class Role(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
