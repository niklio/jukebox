from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework_jwt.views import api_settings
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from accounts.models import UserProfile
from accounts.permissions import IsAdminJWT, IsMyJWT
from accounts.serializers import UserSerializer, UserProfileSerializer


class AccountViewSet(viewsets.ModelViewSet):

    serializer_class = UserProfileSerializer
    queryset = User.objects.all()

    def list(self, request):
        try:
            token = request.META['HTTP_AUTHORIZATION']
            token = token.split(' ')[-1]
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = VerifyJSONWebTokenSerializer()

        serialized = serializer.validate({"token": token})
        username = serialized['user']

        user = User.objects.get(username=username)
        if not user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)

        queryset = UserProfile.objects.all()
        serializer = UserProfileSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serialized = UserSerializer(data=request.data)
        if serialized.is_valid():
            user = User.objects.create_user(
                serialized.data['username'],
                serialized.data['email'],
                serialized.data['password']
            )

            UserProfile.create_profile(user)

            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            return Response({"token": token}, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        serializer = VerifyJSONWebTokenSerializer()
        queryset = User.objects.all()
        user = get_object_or_404(queryset, username=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)


