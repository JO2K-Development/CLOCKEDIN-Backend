from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .invitation_view import InvitationViewSet
from .user_view import UserViewSet
from .working_status_view import WorkStatusViewSet

router = DefaultRouter()
router.register(r"", UserViewSet, basename="user")
router.register(r"invitations", InvitationViewSet, basename="invitation")
router.register(r"work-status", WorkStatusViewSet, basename="work-status")

urlpatterns = [
    path("", include(router.urls)),
]
