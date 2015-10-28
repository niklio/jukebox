from rest_framework import serializers

from songs.models import Song

class SongSerializer(serializers.ModelSerializer):

    class Meta:
        model = Song
        fields = (
            'id',
            'song_id',
            'title',
            'duration',
            'stream_url',
            'artwork_url',
            'played',
            'pod',
            'submitted_by'
        )