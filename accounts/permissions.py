from rest_framework.permissions import BasePermission

class IsCreationOrIsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return view.action == 'create' or request.user.is_authenticated()