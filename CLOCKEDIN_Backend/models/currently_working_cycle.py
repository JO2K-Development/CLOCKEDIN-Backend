from django.db import models

from CLOCKEDIN_Backend.models.company import Company
from CLOCKEDIN_Backend.models.user import User


class CurrentlyWorkingCycle(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='current_work_cycles')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    START_METHOD_CHOICES = [
        ('manual', 'Manual'),
        ('auto', 'Automatic'),
    ]
    start_method = models.CharField(max_length=20, choices=START_METHOD_CHOICES)

    def __str__(self):
        return f"{self.employee} started working at {self.start_time}"
