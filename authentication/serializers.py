from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from rest_framework import serializers

from authentication.models import Account, Membership
from pods.models import Pod


class AccountSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=False)

    pods = serializers.SlugRelatedField(
        many=True,
        read_only=False,
        queryset=Pod.objects.all(),
        slug_field='name',
    )

    class Meta:
        model = Account
        fields = (
            'id',
            'username',
            'pods',
            'created_at',
            'updated_at',
            'password',
        )
        read_only_fields = (
            'id',
            'pods',
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


class MembershipSerializer(serializers.ModelSerializer):

    class Meta:
        model = Membership
        fields = (
            'pod',
            'account',
            'date_joined',
            'invite_pending',
        )
        read_only_fields = (
            'pod',
            'account',
            'date_joined',
            'invite_pending',
        )