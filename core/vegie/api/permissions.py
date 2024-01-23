from rest_framework import permissions


class CustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ('POST', 'PUT', 'DELETE'):
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in ('PUT', 'DELETE'):
            return obj.user == request.user
        return True
