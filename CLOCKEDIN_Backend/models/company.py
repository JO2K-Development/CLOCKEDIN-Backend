from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255)
    company_logo_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
