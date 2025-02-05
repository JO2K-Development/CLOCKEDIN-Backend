from django.urls import include, path
from rest_framework.routers import DefaultRouter

from CLOCKEDIN_Backend.views.user.company_view import CreateCompanyView
from CLOCKEDIN_Backend.views.user.invitation_view import InvitationViewSet
from CLOCKEDIN_Backend.views.user.user_view import UserView
from CLOCKEDIN_Backend.views.user.work_cycles_view import WorkCyclesViewSet
from CLOCKEDIN_Backend.views.user.work_status_view import WorkStatusViewSet

router = DefaultRouter()
router.register(r"invitations", InvitationViewSet, basename="invitation")
router.register(r"work-status", WorkStatusViewSet, basename="work-status")
router.register(r"work-cycles", WorkCyclesViewSet, basename="work-cycles")


urlpatterns = [
    path("", include(router.urls)),
    path("create-company/", CreateCompanyView.as_view(), name="create-company"),
    path("user/", UserView.as_view(), name="user-detail"),
]
