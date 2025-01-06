from django.urls import path

from CLOCKEDIN_Backend.views.admin.views import EmployeeStatusView, InviteView, RemoveEmployeeView

urlpatterns = [
    path("invite/", InviteView.as_view(), name="invite"),
    path("remove-employee/", RemoveEmployeeView.as_view(), name="remove-employee"),
    path("employee-status/", EmployeeStatusView.as_view(), name="employee-status"),
]
