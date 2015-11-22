from django.shortcuts import render, get_object_or_404

from rest_framework import permissions, viewsets, views, status
from rest_framework.response import Response

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

import soundcloud

from authentication.models import Account
from pods.models import Pod
from songs.models import Song
from songs.permissions import IsSubmitter
from songs.serializers import SongSerializer

client = soundcloud.Client(client_id='13b1f6ea8ef9dd2d629f3c0e1707f16b')

class NextSong(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, name):
        queryset = Pod.objects.all()
        pod = get_object_or_404(queryset, name=name)

        songs = pod.songs.filter(queued=True).order_by('id')
        if not songs.exists():
            return Response({
                'status': 'not found',
                'message': 'No songs in queue'
            }, status=status.HTTP_404_NOT_FOUND)

        next = songs[0]
        next.played = True
        next.save()

        track = client.get('tracks', id=next.song_id)
        stream_url = client.get(track.stream_url, allow_redirects=False)

        data = SongSerializer(next).data
        data.update({'stream_url': stream_url.location})

        return Response(data)


class SongViewSet(viewsets.ViewSet):
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


    def list(self, request, account_name=None, pod_name=None):
        queryset = Song.objects.all()

        if account_name:
            queryset.filter(submitted_by=account_name)

        if pod_name:
            queryset.filter(pod=pod_name)

        queryset.filter(queued=True)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


    def create(self, request, account_name=None, pod_name=None):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        if not account_name:
            account_name = serializer.validated_data['submitted_by']

        if not pod_name:
            pod_name = serializer.validated_data['pod']

        account = Account.objects.get(username=account_name)
        pod = Pod.objects.get(name=pod_name)

        if account.username != request.user.username:
            return Response({
                'status': 'Forbidden',
                'message': 'You do not have permission to submit a song as this user.'
            }, status=status.HTTP_403_FORBIDDEN)

        if not account.pods.filter(id=pod.id):
            return Response({
                'status': 'Forbidden',
                'message': 'You do not have permission to submit a song to this pod.'
            }, status=status.HTTP_403_FORBIDDEN)

        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


    def retrieve(self, request, id=None, account_name=None, pod_name=None):
        queryset = Song.objects.all()

        if account_name:
            queryset.filter(submitted_by=account_name)

        if pod_name:
            queryset.filter(pod=pod_name)

        song = get_object_or_404(queryset, id=id)
        serializer = self.serializer_class(song)
        return Response(serializer.data)