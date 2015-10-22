from rest_framework import serializers
from pods.models import Pod

class PodSerializer(serializers.ModelSerializer):

    qr_code_url = serializers.ReadOnlyField()

    class Meta:
        model = Pod
        fields = ('id', 'host', 'qr_code_url')