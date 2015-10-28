from rest_framework import serializers

from authentication.models import Account
from pods.models import Pod

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
    
    class Meta:
        model = Pod
        fields = ('id', 'host', 'members', 'name')
