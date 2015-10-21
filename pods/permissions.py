from rest_framework.permissions import BasePermission
from accounts.models import UserProfile

class IsMemberOf(BasePermission):

    def has_permission(self, request, view):

        return request.user.pod == request.pod.id