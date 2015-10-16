class PodSerializer(serializers.ModelSerializer):

    qr_code_url = serializers.ReadOnlyField()

    class Meta:
        model = Pod
        fields = ('id', 'host', 'qr_code_url')