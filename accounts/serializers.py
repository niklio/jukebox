from rest_framework import serializers
from django.contrib.auth.models import User

from models import UserProfile

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileSerializer(serializers.ModelSerializer):

    pod = serializers.PrimaryKeyRelatedField(source='pod_id', read_only=True)

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'email', 'pod', 'is_host')
