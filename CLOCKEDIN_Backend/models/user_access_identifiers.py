from django.db import models

from CLOCKEDIN_Backend.models.access_identifier import AccessIdentifier
from CLOCKEDIN_Backend.models.user import User


class UserAccessIdentifier(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(AccessIdentifier, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'role')

    def __str__(self):
        return f"{self.user} - {self.role}"
