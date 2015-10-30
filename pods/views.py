from django.shortcuts import render, get_object_or_404

from rest_framework import permissions, viewsets, status
from rest_framework.response import Response

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.decorators import detail_route, list_route

from authentication.models import Account
from pods.models import Pod
from pods.serializers import PodSerializer
from pods.permissions import IsHost, IsMember

class PodViewSet(viewsets.ViewSet):
    """
    API endpoint that allows pods to be viewed or edited.
    """
    lookup_field = 'name'
    authentication_classes = (JSONWebTokenAuthentication,)
    queryset = Pod.objects.all()
    serializer_class = PodSerializer


    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.IsAuthenticated(),)

        if self.request.method == 'POST':
            return (permissions.IsAuthenticated(),)

        if self.request.method == 'DELETE':
            return (permissions.IsAuthenticated(), IsHost())

        return (permissions.IsAuthenticated(), IsMember())


    def list(self, request):
        queryset = self.queryset
        serializer = PodSerializer(queryset, many=True)
        return Response(serializer.data)


    def retrieve(self, request, name=None):
        pod = get_object_or_404(self.queryset, name=name)
        serializer = PodSerializer(pod)
        return Response(serializer.data)


    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        account = Account.objects.get(username=serializer.validated_data['host'])

        if account.username != request.user.username:
            return Response({
                'status': 'Forbidden',
                'message': 'You do not have permission to create a pod hosted by user: {}.'.format(account.username)
            }, status=status.HTTP_403_FORBIDDEN)

        if account.is_host:
            return Response({
                'status': 'Forbidden',
                'message': 'You already host a pod.'
            })

        pod = serializer.save()
        account.pods.add(pod)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


    def update(self, request, name=None):
        pod = get_object_or_404(self.queryset, name=name)
        serializer = self.serializer_class(pod, data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        name, host, members = serializer.validated_data.values()

        # The host can change pod name
        if name:
            if request.user == pod.host:
                pod.name = name
            else:
                if name != pod.name:
                    return Response({
                        'status': 'Forbidden',
                        'message': 'Only the host may change the name of their pod.'
                    }, status=status.HTTP_403_FORBIDDEN)


        # The host can pass pod to a user without a hosted pod
        if host:
            if request.user == pod.host:
                if host.is_host:
                    return Response({
                        'status': 'Forbidden',
                        'message': 'This user already hosts a pod'
                    }, status=status.HTTP_403_FORBIDDEN)
                else:
                    pod.host = host
            else:
                if host != pod.host:
                    return Response({
                        'status': 'Forbidden',
                        'message': 'Only the host may change the name of their pod.'
                    })

        # The host can add AND remove users from his pod
        if members:
            if request.user == pod.host:
                pod.members = members
            else:
                for member in members:
                    pod.members.add(member)

        pod.save()
        pod.host.pods.add(pod)

        return Response(pod, status=status.HTTP_200_OK)