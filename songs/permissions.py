from rest_framework import permissions

class IsSubmitter(permissions.BasePermission):
    def has_object_permission(self, request, view, song):
        return request.user == song.submitted_by
