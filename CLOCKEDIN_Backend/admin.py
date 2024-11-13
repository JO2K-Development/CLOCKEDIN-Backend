from django.contrib import admin

from CLOCKEDIN_Backend.models import (
    AccessIdentifier,
    Company,
    CurrentWorkCycle,
    User,
    UserAccessIdentifier,
    Wage,
    WorkCycle,
)
from CLOCKEDIN_Backend.models.invitation import Invitation

admin.site.register(Company)
admin.site.register(User)
admin.site.register(CurrentWorkCycle)
admin.site.register(WorkCycle)
admin.site.register(AccessIdentifier)
admin.site.register(UserAccessIdentifier)
admin.site.register(Wage)
admin.site.register(Invitation)
