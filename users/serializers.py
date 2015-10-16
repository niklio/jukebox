from rest_framework import serializers
from django.contrib.auth.models import User

from models import UserProfile

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileSerializer(serializers.ModelSerializer):
    is_host = serializers.Field()
    pod = serializers.PrimaryKeyRelatedField(source='pod_id', read_only=True)

    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'pod', 'is_host')