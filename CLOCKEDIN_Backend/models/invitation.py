from django.db import models

from .company import Company


class Invitation(models.Model):
    email = models.EmailField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    position = models.CharField(max_length=50, default="Employee")
    roles = models.ManyToManyField("Role", blank=True)
    status = models.CharField(max_length=20, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
