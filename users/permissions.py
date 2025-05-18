from rest_framework import permissions


class ItsModer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderators").exists()


class ItsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False
