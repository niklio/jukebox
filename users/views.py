from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework_jwt.views import api_settings
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

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        return Response({"token": token}, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer