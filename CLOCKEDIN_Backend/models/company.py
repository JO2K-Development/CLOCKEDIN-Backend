from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey('User', null=True, on_delete=models.PROTECT, related_name='owned_companies')
    company_logo_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
