from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .invitation_view import InvitationViewSet
from .user_view import UserViewSet
from .work_cycles_view import WorkCyclesViewSet
from .work_status_view import WorkStatusViewSet

router = DefaultRouter()
router.register(r"user", UserViewSet, basename="user")
router.register(r"invitations", InvitationViewSet, basename="invitation")
router.register(r"work-status", WorkStatusViewSet, basename="work-status")
router.register(r"work-cycles", WorkCyclesViewSet, basename="work-cycles")


urlpatterns = [
    path("", include(router.urls)),
]
