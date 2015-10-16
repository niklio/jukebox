from django.contrib.auth.models import User
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from rest_framework_jwt.views import api_settings

class IsAdminJWT(BaseJSONWebTokenAuthentication):

    def has_permission(self, request, view):

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