from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from accounts.models import UserProfile
from pods.serializers import PodSerializer
from pods.models import Pod

class PodViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )
    serializer_class = PodSerializer
    queryset = Pod.objects.all()

    def list(self, request):
        serializer = PodSerializer(self.queryset, many=True)

        if request.user.is_superuser:
            return Response(serializer.data);
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def create(self, request):

        serializer = PodSerializer(data={
            'host': request.user.profile.id
        })

        if serializer.is_valid():
            pod = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request):
        pass

    def retrieve(self, request):
        pass