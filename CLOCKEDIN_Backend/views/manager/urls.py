from django.urls import path

from CLOCKEDIN_Backend.views.manager.invitation_view import InviteView

urlpatterns = [
    path("invite/", InviteView.as_view(), name="invite"),
]
