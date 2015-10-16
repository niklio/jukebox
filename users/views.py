from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from users.models import UserProfile
from users.serializers import UserSerializer, UserProfileSerializer


@api_view(['POST'])
def register(request):
    serialized = UserSerializer(data=request.data)
    if serialized.is_valid():
        user = User.objects.create_user(
            serialized.data['username'],
            serialized.data['email'],
            serialized.data['password']
        )
        UserProfile.create_profile(user)
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


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



