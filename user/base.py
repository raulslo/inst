from rest_framework import permissions


class UpdateOwnUser(permissions.BasePermission):

    def has_object_permission(self, request, view, object):

        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.id == object.id


class UpdateOwnProfile(permissions.BasePermission):

    def has_object_permission(self, request, view, object):

        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.id == object.user.id
