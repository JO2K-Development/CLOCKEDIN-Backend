# from django.db import models
# from django.db.models import Q
#
# class EmailAddress(models.Model):
#     email = models.EmailField(unique=True)
#     is_primary = models.BooleanField(default=False)
#
#     class Meta:
#         constraints = [
#             models.UniqueConstraint(
#                 fields=['email'],
#                 condition=Q(is_primary=True),
#                 name='unique_primary_email'
#             )
#         ]