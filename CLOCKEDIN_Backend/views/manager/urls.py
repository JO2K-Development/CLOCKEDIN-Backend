from django.urls import path

from CLOCKEDIN_Backend.views.manager.invitation_view import InviteViewSet

urlpatterns = [
    path("invite/", InviteViewSet.as_view(), name="invite"),
]
