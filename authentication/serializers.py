from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from rest_framework import serializers

from authentication.models import Account
from songs.models import Song


class AccountSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=False)

    submitted_songs = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='id',
    )


    class Meta:
        model = Account
        fields = (
            'id',
            'username',
            'pods',
            'is_host',
            'created_at',
            'updated_at',
            'password',
            'submitted_songs',
        )
        read_only_fields = (
            'pods',
            'is_host',
            'created_at',
            'updated_at',
        )


        def create(self, validated_data):
            return Account.objects.create(**validated_data)


        def update(self, instance, validated_data):
            password = validated_data.get('password', None)

            if password:
                instance.set_instance(password)
                instance.save()

            return instance
    