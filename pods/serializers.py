from rest_framework import serializers

from authentication.models import Account
from pods.models import Pod
from songs.models import Song

class PodSerializer(serializers.ModelSerializer):

    host = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field='username',
        queryset=Account.objects.all()
    )

    members = serializers.SlugRelatedField(
        many=True,
        read_only=False,
        slug_field='username',
        queryset=Account.objects.all()
    )

    songs = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='id',
    )
    
    
    class Meta:
        model = Pod
        fields = (
            'id',
            'name',
            'host',
            'members',
            'songs',
        )


    def create(self, validated_data):
        members = validated_data.pop('members')
        instance = Pod.objects.create(**validated_data)

        instance.host.pods.add(instance)
        instance.host.save()

        for member in members:
            member.pods.add(instance)
            member.save()

        return instance


    def update(self, instance, validated_data):
        members = validated_data['members']

        for member in members:
            member.pods.add(instance)
            member.save()

        return instance.save()

