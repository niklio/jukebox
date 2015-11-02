from datetime import datetime

from django.shortcuts import render, get_object_or_404

from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.decorators import detail_route, list_route

from guardian.shortcuts import assign_perm, get_perms

from authentication.models import Account, Membership
from pods.models import Pod
from pods.serializers import PodSerializer

host_permissions = ['add_user', 'remove_user', 'change_user_permissions', 'manage_pod', 'delete_pod']
user_permissions = ['add_user']


class PodViewSet(viewsets.ViewSet):
    """
    API endpoint that allows pods to be viewed or edited.
    """
    lookup_field = 'name'
    authentication_classes = (JSONWebTokenAuthentication,)
    queryset = Pod.objects.all()
    serializer_class = PodSerializer

    def get_permissions(self):
        return permissions.IsAuthenticated(),

    def list(self, request):
        queryset = Pod.objects.all()
        serializer = PodSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, name=None):
        pod = get_object_or_404(self.queryset, name=name)
        serializer = PodSerializer(pod)
        return Response(serializer.data)

    def create(self, request):
        # Serialize data into pod.
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        print serializer.validated_data
        pod = serializer.save()

        # Make the user a host of the pod.
        account = request.user
        for permission in host_permissions:
            assign_perm(permission, account, pod)
        Membership.objects.create(pod=pod, account=account, date_joined=datetime.now(), invite_pending=False,
                                  playing_songs=False)
        account.save()

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

        print serializer.validated_data.values()
        name, members = serializer.validated_data.values()

        # Change the pod name.
        if pod.name != name:
            if request.user.has_perm('pods.manage_pod', pod):
                pod.name = name
            else:
                return Response({
                    'status': 'Forbidden',
                    'message': 'You do not have the permission to manage pod settings.'
                }, status=status.HTTP_403_FORBIDDEN)

        # Add and remove users from the pod.
        current = set(pod.members.all())
        suggested = set(members)
        removed = current - suggested
        added = suggested - current

        # Check if the adding/removing user has permissions to add/remove.
        if added and not request.user.has_perm('pods.add_user', pod):
            return Response({
                'status': 'Forbidden',
                'message': 'You do not have the permission to add users to the pod.'
            }, status=status.HTTP_403_FORBIDDEN)

        if removed and not request.user.has_perm('pods.remove_user', pod):
            return Response({
                'status': 'Forbidden',
                'message': 'You do not have the permission to remove users from the pod.'
            }, status=status.HTTP_403_FORBIDDEN)

        # Add users.
        for account in added:
            for permission in user_permissions:
                assign_perm(permission, account, pod)
                account.save()
            Membership.objects.create(pod=pod, account=account, date_joined=datetime.now(), invite_pending=False,
                                      playing_songs=False)

        # Remove users.
        Membership.objects.filter(account__in=removed).delete()

        pod.save()

        serializer = PodSerializer(pod)
        return Response(serializer.data)

    def destroy(self, request, name=None):
        pod = get_object_or_404(self.queryset, name=name)
        if request.user.has_perm('pods.delete_pod', pod):
            pod.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({
            'status': 'Forbidden',
            'message': 'You do not have the permission to delete the pod.'
        }, status=status.HTTP_403_FORBIDDEN)