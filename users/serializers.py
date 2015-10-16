from rest_framework import serializers

from models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    is_host = serializers.Field()
    pod = serializers.PrimaryKeyRelatedField(source='pod_id')

    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'pod', 'is_host')