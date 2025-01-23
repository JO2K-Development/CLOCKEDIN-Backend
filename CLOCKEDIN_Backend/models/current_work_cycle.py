from django.db import models

from CLOCKEDIN_Backend.models.company import Company
from CLOCKEDIN_Backend.models.user import User


class WorkCycleActionType(models.TextChoices):
    QR_CODE = "qr_code", "QR Code"
    APP = "app", "App"


class CurrentWorkCycle(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="current_work_cycles")
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    start_method = models.CharField(max_length=20, choices=WorkCycleActionType.choices)

    def __str__(self):
        return f"{self.employee} started working at {self.start_time}"
