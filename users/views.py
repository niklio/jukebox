from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from users.models import UserProfile
from users.serializer import UserProfileSerializer
 
# class RestrictedView(APIView):
#     permission_classes = (IsAuthenticated, )
#     authentication_classes = (JSONWebTokenAuthentication, )
 
#     def get(self, request):
#         data = {
#             'id': request.user.id,
#             'username': request.user.username,
#             'token': str(request.auth)
#         }
#         return Response(data)

class UserView(APIView):
    """
    Base APIView class for endpoints that need to access
    the UserProfile object behind a user.
    """
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )

    def initial(self, request, *args, **kwargs):
        out = super(UserView, self).initial(request, *args, **kwargs)

        try:
            profile = UserProfile.objects.get(user__id=request.user.id)
        except UserProfile.DoesNotExist:
            self.permission_denied(request)

        self.profile = profile
        return out

class UserProfileView(UserView):
    """
    Detailed information about the current user.

    GET - get the serialized form of the user.
    PATCH - set attributes of the logged in user.
    """

    def get(self, request, *args, **kwargs):
        serializer = UserProfileSerializer(self.profile)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        serializer = UserProfileSerializer(
            self.profile,
            partial=True,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)