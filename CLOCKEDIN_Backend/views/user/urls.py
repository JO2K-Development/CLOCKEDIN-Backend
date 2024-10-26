from django.urls import path

from CLOCKEDIN_Backend.views.user.views import InvitationView, UserView

urlpatterns = [
    path("", UserView.as_view(), name="user_operations"),
    path("choose-company/", InvitationView.as_view(), name="choose_company"),
]
