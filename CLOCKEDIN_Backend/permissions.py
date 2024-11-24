from rest_framework.permissions import BasePermission

from CLOCKEDIN_Backend.models import RoleEnum


class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and RoleEnum.Employee.value == request.user.role.id)


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and RoleEnum.Manager.value == request.user.role.id)


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and RoleEnum.Admin.value == request.user.role.id)


class IsAtLeastEmployee(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and (
                RoleEnum.Employee.value == request.user.role.id
                or RoleEnum.Manager.value == request.user.role.id
                or RoleEnum.Admin.value == request.user.role.id
            )
        )


class IsAtLeastManager(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and (RoleEnum.Manager.value == request.user.role.id or RoleEnum.Admin.value == request.user.role.id)
        )
