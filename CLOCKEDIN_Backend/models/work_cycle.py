from django.db import models

from CLOCKEDIN_Backend.models.company import Company
from CLOCKEDIN_Backend.models.user import User


class WorkCycle(models.Model):
    employee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="work_cycles"
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    START_METHOD_CHOICES = [
        ("manual", "Manual"),
        ("auto", "Automatic"),
    ]
    start_method = models.CharField(max_length=20, choices=START_METHOD_CHOICES)
    END_METHOD_CHOICES = [
        ("manual", "Manual"),
        ("auto", "Automatic"),
    ]
    end_method = models.CharField(max_length=20, choices=END_METHOD_CHOICES)
    is_confirmed_stationary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee} worked from {self.start_time} to {self.end_time}"
