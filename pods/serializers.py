from rest_framework import serializers

from authentication.models import Account
from pods.models import Pod

class PodSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Pod
        fields = ('id', 'host', 'members', 'name')
