from rest_framework import serializers

from authentication.models import Account
from pods.models import Pod
from songs.models import Song

class SongSerializer(serializers.ModelSerializer):

    pod = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field='name',
        queryset=Pod.objects.all()
    )
    submitted_by = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field='username',
        queryset=Account.objects.all()
    )


    class Meta:
        model = Song
        fields = (
            'id',
            'song_id',
            'title',
            'album',
            'artist',
            'queued',
            'pod',
            'submitted_by'
        )
        read_only_fields = (
            'queued',
        )