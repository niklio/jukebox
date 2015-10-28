from django.shortcuts import render

from rest_framework import permissions, viewsets, status
from rest_framework.response import Response

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from songs.models import Song
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