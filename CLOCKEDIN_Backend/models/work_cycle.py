from django.db import models
from django.utils import timezone

from CLOCKEDIN_Backend.models import Company, User


class WorkCycleActionType(models.TextChoices):
    QR_CODE = "qr_code", "QR Code"
    APP = "app", "App"


class WorkCycle(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="work_cycles")
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    start_method = models.CharField(max_length=20, choices=WorkCycleActionType.choices)
    end_method = models.CharField(max_length=20, choices=WorkCycleActionType.choices)
    is_confirmed_stationary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def duration(self):
        if self.end_time and self.start_time:
            return self.end_time - self.start_time
        return timezone.timedelta(0)

    def __str__(self):
        return f"{self.employee} worked from {self.start_time} to {self.end_time}"
