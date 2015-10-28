from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from rest_framework import serializers

from authentication.models import Account


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Account
        fields = ('id', 'username', 'pod', 'is_host', 'created_at', 'updated_at', 'password')
        read_only_fields = ('pod', 'is_host', 'created_at', 'updated_at')

        def create(self, validated_data):
            return Account.objects.create(**validated_data)

        def update(self, instance, validated_data):
            password = validated_data.get('password', None)

            if password:
                instance.set_instance(password)
                instance.save()

            return instance
    