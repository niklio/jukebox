from rest_framework.viewsets import ModelViewSet
from pods.serializers import PodSerializer
from pods.models import Pod
from accounts.models import UserProfile
from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

class PodViewSet(ModelViewSet):
    permission_classes = ()
    authentication_classes = (JSONWebTokenAuthentication, )
    serializer_class = PodSerializer
    queryset = Pod.objects.all()

    def list(self, request):
        serializer = PodSerializer(self.queryset, many=True)

        if request.user.is_superuser:
            return Response(serializer.data);
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def create(self, request):
        host = UserProfile.objects.get(username=request.user)
        print host.id
        data = {'host': host.id, 'name': request.name}
        serializer = PodSerializer(data=data)
        if serializer.is_valid():
            pod = serializer.save()
            return Response({"location": ("/api/pods/" + str(pod.id))}, status=status.HTTP_201_CREATED)
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request):
        pass

    def retrieve(self, request):
        pass