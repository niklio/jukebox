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
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)
    queryset = Pod.objects.all()
    serializer_class = PodSerializer

    def create(self, request):
        request.data.update({'host': request.user.id})
        serializer = self.serializer_class(data = request.data)

        print serializer.is_valid()
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)