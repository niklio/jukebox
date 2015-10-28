from django.shortcuts import render

from rest_framework import permissions, viewsets, status
from rest_framework.response import Response

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from pods.models import Pod
from pods.serializers import PodSerializer


class PodViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows pods to be viewed or edited.
    """
    lookup_field = 'name'
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)
    queryset = Pod.objects.all()
    serializer_class = PodSerializer


    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response({
                'status': 'Bad request',
                'message': 'Pod could not be created with received data'
            }, status=status.HTTP_400_BAD_REQUEST)

        if serializer.data['host'] != request.user.username:
            return Response({
                'status': 'Unauthorized',
                'message': 'Not authorized to create a pod hosted by {}. Check your authentication header'.format(serializer.data['host'])
            }, status=status.HTTP_401_UNAUTHORIZED)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
