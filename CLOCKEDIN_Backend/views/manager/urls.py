from django.urls import path, include
from rest_framework.routers import DefaultRouter

from CLOCKEDIN_Backend.views.manager.invitation_view import InvitationViewSet

router = DefaultRouter()
router.register(r"invitations", InvitationViewSet, basename="invitation")


urlpatterns = [
    path("", include(router.urls)),
]
