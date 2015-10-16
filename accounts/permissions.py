from django.contrib.auth.models import User
from rest_framework.permissions import BasePermission
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from rest_framework_jwt.views import api_settings

def IsAdminJWT(request):
    try:
        token = request.META['HTTP_AUTHORIZATION']
        token = token.split(' ')[-1]
    except:
        return False

    serializer = VerifyJSONWebTokenSerializer()

    serialized = serializer.validate({"token": token})
    username = serialized['user']

    user = User.objects.get(username=username)
    return user.is_superuser


class IsMyJWT(BasePermission):

    def has_permission(request, pk):
        try:
            token = request.META['HTTP_AUTHORIZATION']
            token = token.split(' ')[-1]
        except:
            return False

        serializer = VerifyJSONWebTokenSerializer()

        print request.data