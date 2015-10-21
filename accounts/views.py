from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework_jwt.views import api_settings
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from accounts.models import UserProfile
from accounts.permissions import IsCreationOrIsAuthenticated
from accounts.serializers import UserSerializer, UserProfileSerializer

class AccountViewSet(ModelViewSet):

    permission_classes = (IsCreationOrIsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

    def list(self, request):
        serializer = UserProfileSerializer(queryset, many=True)

        if request.user.is_superuser:
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            UserProfile.create_profile(user)

            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            return Response({"token": token}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        profile = get_object_or_404(queryset, username=pk)
        serializer = UserProfileSerializer(profile)

        if request.user.is_superuser or request.user == profile.user:
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


    def destroy(self, request, pk=None):
        user = User.objects.get(username=pk)
        profile = UserProfile.objects.get(username=pk)
        
        if profile or user:
            if request.user.is_superuser or request.user == profile.user:
                profile.delete()
                user.delete()
                return Response(status=status.HTTP_202_ACCEPTED)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)