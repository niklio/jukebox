from rest_framework import permissions

class IsMember(permissions.BasePermission):
    def has_object_permission(self, request, view, pod):
        return request.user.pod and request.user.pod == pod

class IsHost(permissions.BasePermission):
    def has_object_permission(self, request, view, pod):
        return request.user == pod.host