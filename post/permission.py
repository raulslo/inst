from rest_framework.permissions import BasePermission
from rest_framework import generics, permissions, mixins, decorators, viewsets


class IsAuthorCommentEntry(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user or obj.entry.group.founder == request.user


class IsAuthor(BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class UpdateOwn(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author.id == request.user.id
