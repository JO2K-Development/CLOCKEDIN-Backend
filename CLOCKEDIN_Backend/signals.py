from django.db.models.signals import post_migrate
from django.dispatch import receiver

from CLOCKEDIN_Backend.models import Role, RoleEnum


@receiver(post_migrate)
def create_default_roles(sender, **kwargs):
    for role in RoleEnum:
        Role.objects.get_or_create(name=role.value)
