from django.db.models.signals import post_migrate
from django.dispatch import receiver

from CLOCKEDIN_Backend.models.role import Role


@receiver(post_migrate)
def create_default_roles(sender, **kwargs):
    Role.objects.get_or_create(name='Admin')
    Role.objects.get_or_create(name='Manager')
    Role.objects.get_or_create(name='Employee')