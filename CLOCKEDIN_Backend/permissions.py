from rest_framework.permissions import BasePermission

from CLOCKEDIN_Backend.models import RoleEnum


class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.roles.filter(name=RoleEnum.Employee.value).exists()
        )


class IsManager(BasePermission):
    def has_permission(self, request, view):
        print(request.user)
        print(request.user.is_authenticated)
        print(request.user.roles.get(name=RoleEnum.Employee.value))
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.roles.filter(name=RoleEnum.Manager.value).exists()
        )


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.roles.filter(name=RoleEnum.Admin.value).exists()
        )
