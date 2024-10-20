from django.contrib import admin

from CLOCKEDIN_Backend.models import Company, User, CurrentlyWorkingCycle, WorkCycle, AccessIdentifier, UserAccessIdentifier, Wage
from CLOCKEDIN_Backend.models.invitation import Invitation

admin.site.register(Company)
admin.site.register(User)
admin.site.register(CurrentlyWorkingCycle)
admin.site.register(WorkCycle)
admin.site.register(AccessIdentifier)
admin.site.register(UserAccessIdentifier)
admin.site.register(Wage)
admin.site.register(Invitation)
