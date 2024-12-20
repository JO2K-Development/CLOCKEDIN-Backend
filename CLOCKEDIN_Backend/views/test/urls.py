from django.urls import path

from CLOCKEDIN_Backend.views.test.not_secured.views import UnsecuredView
from CLOCKEDIN_Backend.views.test.secured.views import SecuredView

urlpatterns = [
    path("secured/", SecuredView.as_view(), name="secured"),
    path("unsecured/", UnsecuredView.as_view(), name="not_secured"),
]
