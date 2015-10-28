from django.shortcuts import render

from rest_framework import permissions, viewsets, status
from rest_framework.response import Response

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from pods.models import Pod
from pods.serializers import PodSerializer

from django.shortcuts import get_object_or_404

class PodViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows pods to be viewed or edited.
    """
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)
    lookup_field = 'name'
    queryset = Pod.objects.all()
    serializer_class = PodSerializer

    def create(self, request):
        print vars(request)
        request.data.update({'host': request.user.id})
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            serializer.save()
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
