from rest_framework.permissions import BasePermission


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and (request.user.role in ["manager"]))


class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and (request.user.role in ["employee"]))


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and (request.user.role in ["admin"]))
