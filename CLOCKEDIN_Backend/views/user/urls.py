from django.urls import path

from CLOCKEDIN_Backend.views.user.views import ChooseCompanyView

urlpatterns = [
    path('choose-company/', ChooseCompanyView.as_view(), name='choose_company'),
]

