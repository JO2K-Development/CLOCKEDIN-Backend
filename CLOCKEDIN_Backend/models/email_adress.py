# models/email_address.py
from django.db import models
from CLOCKEDIN_Backend.models.user import User

class EmailAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_addresses')
    email = models.EmailField(unique=True)
    verified = models.BooleanField(default=False)
