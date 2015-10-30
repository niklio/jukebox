from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from django.shortcuts import get_object_or_404

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
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def create(self, request):
        request.data.update({'host': request.user.profile.id})
        serializer = PodSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            print serializer.data
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers={'Location': ('/api/pods/' + serializer.data['id'])})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        pod = get_object_or_404(self.queryset, id=pk)
        print pod.host_id
        if pod:
            if pod.host_id == request.user.profile.id or request.user.is_superuser:
                pod.delete()
                return Response(status=status.HTTP_202_ACCEPTED)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, pk=None):
        pod = get_object_or_404(self.queryset, id=pk)
        serializer = PodSerializer(pod)
        return Response(serializer.data)
