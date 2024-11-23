from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .invitation_view import InvitationViewSet
from .user_view import UserViewSet
from .work_cycles_view import WorkCyclesViewSet
from .work_status_view import WorkStatusViewSet

router = DefaultRouter()  # Disable trailing slash
router.register(r"", UserViewSet, basename="user")
router.register(r"invitations", InvitationViewSet, basename="invitation")
router.register(r"work-status", WorkStatusViewSet, basename="work-status")
router.register(r"work-cycles", WorkCyclesViewSet, basename="work-cycles")


urlpatterns = [
    path("", include(router.urls)),

]
# re_path(r"^work-cycles$", WorkCyclesViewSet.as_view({'get': 'list'}), name='work-cycles-list'),
    # re_path(r"^work-cycles\.(?P<format>[a-z0-9]+)/?$", WorkCyclesViewSet.as_view({'get': 'list'}), name='work-cycles-list'),
    # re_path(r"^work-cycles/(?P<pk>[^/.]+)$", WorkCyclesViewSet.as_view({'get': 'retrieve'}), name='work-cycles-detail'),
    # re_path(r"^work-cycles/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$", WorkCyclesViewSet.as_view({'get': 'retrieve'}), name='work-cycles-detail'),