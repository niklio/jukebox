from rest_framework import serializers

from authentication.models import Account
from pods.models import Pod
from songs.models import Song

class PodSerializer(serializers.ModelSerializer):

    members = serializers.SlugRelatedField(
        many=True,
        read_only=False,
        queryset=Account.objects.all(),
        slug_field='username',
    )

    class Meta:
        model = Pod
        fields = (
            'id',
            'name',
            'members',
        )