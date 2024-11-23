from rest_framework.permissions import BasePermission

from CLOCKEDIN_Backend.models.role import RoleEnum


class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and RoleEnum.EMPLOYEE.value in request.user.roles.values_list('id', flat=True)
        )


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and RoleEnum.MANAGER.value in request.user.roles.values_list('id', flat=True)
        )


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and RoleEnum.ADMIN.value in request.user.roles.values_list('id', flat=True)
        )
