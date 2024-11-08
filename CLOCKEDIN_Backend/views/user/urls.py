from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import InvitationViewSet, UserViewSet

router = DefaultRouter()
router.register(r"", UserViewSet, basename="user")
router.register(r"invitations", InvitationViewSet, basename="invitation")

urlpatterns = [
    path("", include(router.urls)),
]
