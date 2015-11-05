from datetime import datetime

from django.shortcuts import get_object_or_404

from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from guardian.shortcuts import assign_perm, get_perms, get_perms_for_model, get_users_with_perms, remove_perm

from authentication.models import Membership, Account
from authentication.serializers import MembershipSerializer
from pods.models import Pod
from pods.serializers import PodSerializer

host_permissions = ['add_accounts', 'remove_accounts', 'change_account_permissions', 'manage_pod']
user_permissions = ['add_accounts']

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
        
        members = serializer.validated_data.pop('members', None)
        if request.user not in members:
            members.append(request.user)

        pod = serializer.save()

        for account in members:
            for permission in user_permissions:
                assign_perm(permission, account, pod)
                account.save()

            Membership.objects.create(
                pod=pod,
                account=account,
                date_joined=datetime.now(),
                invite_pending=False
            )

        for permission in host_permissions:
            assign_perm(permission, request.user, pod)
            request.user.save()

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
        if added and not request.user.has_perm('pods.add_accounts', pod):
            return Response({
                'status': 'Forbidden',
                'message': 'You do not have the permission to add accounts to the pod.'
            }, status=status.HTTP_403_FORBIDDEN)

        if removed and not request.user.has_perm('pods.remove_accounts', pod):
            return Response({
                'status': 'Forbidden',
                'message': 'You do not have the permission to remove accounts from the pod.'
            }, status=status.HTTP_403_FORBIDDEN)

        # Add users.
        for account in added:
            for permission in user_permissions:
                assign_perm(permission, account, pod)
                account.save()

            Membership.objects.create(
                pod=pod,
                account=account,
                date_joined=datetime.now(),
                invite_pending=False,
            )

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


class PermissionsViewSet(viewsets.ViewSet):
    authentication_classes = (JSONWebTokenAuthentication,)
    queryset = Membership.objects.all()

    def list(self, request, pod_name=None, account_username=None):
        pod = Pod.objects.get(name=pod_name)
        account = Account.objects.get(username=account_username)
        return Response(get_perms(account, pod), status=status.HTTP_200_OK)

    def retrieve(self, request, pod_name=None, account_username=None, pk=None):
        pod = Pod.objects.get(name=pod_name)
        account = Account.objects.get(username=account_username)

        if not get_perms_for_model(Pod).filter(codename=pk).exists():
            return Response({
                'status': 'Bad Request',
                'message': 'The permission is not valid.'
            }, status=status.HTTP_400_BAD_REQUEST)

        if account.has_perm(pk, pod):
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pod_name=None, account_username=None, pk=None):
        pod = Pod.objects.get(name=pod_name)
        account = Account.objects.get(username=account_username)

        if not request.user.has_perm('pods.change_account_permissions', pod):
            return Response({
                'status': 'Forbidden',
                'message': 'You do not have the permission to change permissions to accounts in the pod.'
            }, status=status.HTTP_403_FORBIDDEN)

        if not get_perms_for_model(Pod).filter(codename=pk).exists():
            return Response({
                'status': 'Bad Request',
                'message': 'The permission is not valid. Check the spelling and try again.'
            }, status=status.HTTP_400_BAD_REQUEST)

        assign_perm(pk, account, pod)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pod_name=None, account_username=None, pk=None):
        pod = Pod.objects.get(name=pod_name)
        account = Account.objects.get(username=account_username)

        if not request.user.has_perm('pods.change_account_permissions', pod):
            return Response({
                'status': 'Forbidden',
                'message': 'You do not have the permission to remove permissions from accounts in the pod.'
            }, status=status.HTTP_403_FORBIDDEN)

        if not get_perms_for_model(Pod).filter(codename=pk).exists():
            return Response({
                'status': 'Bad Request',
                'message': 'The permission is not valid. Check the spelling and try again.'
            }, status=status.HTTP_400_BAD_REQUEST)

        if len(filter(lambda user: 'change_account_permissions' in user, get_users_with_perms(pod, attach_perms=True).values())) <= 1:
            return Response({
                'status': 'Bad Request',
                'message': 'The fulfillment of this request would leave no account in the pod with the permission to add account permissions.'
            }, status=status.HTTP_400_BAD_REQUEST)

        if account.has_perm(pk, pod):
            remove_perm(pk, account, pod)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
