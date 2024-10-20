from django.db import models
from .company import Company

class Invitation(models.Model):
    email = models.EmailField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='pending')  # e.g., pending, accepted, declined
    created_at = models.DateTimeField(auto_now_add=True)