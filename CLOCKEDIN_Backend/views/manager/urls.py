from django.urls import include, path
from rest_framework.routers import DefaultRouter

from CLOCKEDIN_Backend.views.manager.employees_view import (
    AssignedUsersView,
    AssignUserToManagerView,
    DetachUserFromManagerView,
    UsersWithoutManagerView,
)
from CLOCKEDIN_Backend.views.manager.invitation_view import InvitationViewSet
from CLOCKEDIN_Backend.views.manager.work_cycles_view import WorkCyclesViewSet

router = DefaultRouter()
router.register(r"invitations", InvitationViewSet, basename="invitation")
router.register(r"work-cycles", WorkCyclesViewSet, basename="workcycle")

urlpatterns = [
    path("", include(router.urls)),
    path("employees/without-manager/", UsersWithoutManagerView.as_view(), name="users-without-manager"),
    path("employees/assign/<int:id>/", AssignUserToManagerView.as_view(), name="assign-user-to-manager"),
    path("employees/detach/<int:id>/", DetachUserFromManagerView.as_view(), name="detach-user-from-manager"),
    path("employees/assigned/", AssignedUsersView.as_view(), name="assigned-users"),
]
