from django.db import models
from django.utils import timezone

from CLOCKEDIN_Backend.models import Company, User


class WorkCycleActionType(models.TextChoices):
    QR_CODE = "qr_code", "QR Code"
    APP = "app", "App"


class WorkCycleStatus(models.TextChoices):
    REMOTE_WORK = "remoteWork", "Remote Work"
    APPROVED_BY_MANAGER = "approvedByManager", "Approved by Manager"
    APPROVED_BY_QR = "approvedByQR", "Approved by QR"
    APPROVED_BY_LOCATION = "approvedByLocation", "Approved by Location"


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

    @property
    def status(self):
        if not self.is_confirmed_stationary:
            return WorkCycleStatus.REMOTE_WORK
        if self.start_method == WorkCycleActionType.APP and self.end_method == WorkCycleActionType.APP:
            return WorkCycleStatus.APPROVED_BY_MANAGER
        if self.start_method == WorkCycleActionType.QR_CODE and self.end_method == WorkCycleActionType.QR_CODE:
            return WorkCycleStatus.APPROVED_BY_QR
        if self.is_confirmed_stationary:
            return WorkCycleStatus.APPROVED_BY_LOCATION
        return None

    def __str__(self):
        return f"{self.employee} worked from {self.start_time} to {self.end_time}"
