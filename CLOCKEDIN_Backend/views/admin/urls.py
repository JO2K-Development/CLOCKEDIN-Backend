from django.urls import path

from CLOCKEDIN_Backend.views.admin.views import InviteView

urlpatterns = [
    path('invite/', InviteView.as_view(), name='invite'),
]