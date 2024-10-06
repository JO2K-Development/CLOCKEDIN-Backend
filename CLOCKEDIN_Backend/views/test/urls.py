from django.urls import path

from CLOCKEDIN_Backend.views.test.not_secured.views import NotSecuredView
from CLOCKEDIN_Backend.views.test.secured.views import SecuredView

urlpatterns = [
    path('secured/', SecuredView.as_view(), name='secured'),
    path('not-secured/', NotSecuredView.as_view(), name='not_secured'),
]