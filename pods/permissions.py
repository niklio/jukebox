from rest_framework import permissions

class IsMember(permissions.BasePermission):
    def has_object_permission(self, request, view, pod):
        return request.user.pods and request.user.pods.filter(id=pod.id).exists()

class IsHost(permissions.BasePermission):
    def has_object_permission(self, request, view, pod):
        return request.user == pod.host