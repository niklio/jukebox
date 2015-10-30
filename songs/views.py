from django.shortcuts import render

from rest_framework import permissions, viewsets, status
from rest_framework.response import Response

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from authentication.models import Account
from pods.models import Pod
from songs.models import Song
from songs.permissions import IsSubmitter
from songs.serializers import SongSerializer


class SongViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows songs to be viewed or edited.
    """
    lookup_field = 'id'
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)
    queryset = Song.objects.all()
    serializer_class = SongSerializer


    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.IsAuthenticated(),)

        if self.request.method == 'POST':
            return (permissions.IsAuthenticated(),)

        return (permissions.IsAuthenticated(), IsSubmitter())


    def list(self, request, account_username=None, pod_name=None):
        queryset = self.queryset

        if account_username:
            account = Account.objects.get(username=account_username)
            queryset = queryset.filter(submitted_by=account)

        if pod_name:
            pod = Pod.objects.get(name=pod_name)
            queryset = queryset.filter(pod=pod)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        account = Account.objects.get(username=serializer.validated_data['submitted_by'])
        pod = Pod.objects.get(name=serializer.validated_data['pod'])

        if account.username != request.user.username:
            return Response({
                'status': 'Forbidden',
                'message': 'You do not have permission to submit a song as user: {}.'.format(account.username)
            }, status=status.HTTP_403_FORBIDDEN)

        if not account.pod or account.pod.name != pod.name:
            return Response({
                'status': 'Forbidden',
                'message': 'You do not have permission to submit a song to pod: {}'.format(pod.name)
            }, status=status.HTTP_403_FORBIDDEN)

        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers={'Location': '/api/songs/{0}'.format(serializer.data['id'])}
        )
