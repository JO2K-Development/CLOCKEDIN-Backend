from django.urls import include, path
from rest_framework.routers import DefaultRouter

from CLOCKEDIN_Backend.views.manager.employees_view import ManageEmployeesView
from CLOCKEDIN_Backend.views.manager.invitation_view import InvitationViewSet
from CLOCKEDIN_Backend.views.manager.work_cycles_view import WorkCyclesViewSet

router = DefaultRouter()
router.register(r"invitations", InvitationViewSet, basename="invitation")
router.register(r"work-cycles", WorkCyclesViewSet, basename="workcycle")
router.register(r"employees", ManageEmployeesView, basename="employee")

urlpatterns = [
    path("", include(router.urls)),
]
