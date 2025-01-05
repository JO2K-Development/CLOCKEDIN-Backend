from django.db import models

from CLOCKEDIN_Backend.models.company import Company
from CLOCKEDIN_Backend.models.role import Role


class InvitationStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    ACCEPTED = "accepted", "Accepted"
    REJECTED = "rejected", "Rejected"


class Invitation(models.Model):
    email = models.EmailField()
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    position = models.CharField(max_length=50, default="Employee")
    roles = models.ManyToManyField(Role, blank=True)
    status = models.CharField(max_length=20, choices=InvitationStatus.choices, default=InvitationStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
