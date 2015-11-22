from rest_framework import permissions, viewsets, status
from rest_framework.response import Response

from authentication.models import Account, Membership
from authentication.permissions import IsAccountOwner
from authentication.serializers import AccountSerializer
from pods.models import Pod

from guardian.shortcuts import assign_perm, get_perms

from collections import defaultdict

permissions_list = ['change_account_permissions', 'delete_pod', 'manage_pod', 'remove_accounts', 'add_accounts']

class AccountViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows accounts to be viewed or edited.
    """
    lookup_field = 'username'
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return permissions.AllowAny(),

        if self.request.method == 'POST':
            return permissions.AllowAny(),

        return permissions.IsAuthenticated(), IsAccountOwner()

    def list(self, request, pod_name=None):
        queryset = Account.objects.all()
        
        if pod_name:
            pod = Pod.objects.get(name=pod_name)
            queryset = map(lambda membership: membership.account, Membership.objects.filter(pod=pod))

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            account = Account.objects.create_user(**serializer.validated_data)

            return Response(
                serializer.validated_data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, username=None):
        account = Account.objects.get(username=username)
        memberships = Membership.objects.filter(account=account).all()

        pods = [membership.pod for membership in memberships]
        for pod in pods:
            permissions_hashmap = defaultdict(int)
            pod_members = [membership.account for membership in Membership.objects.filter(pod=pod)]
            for member in pod_members:
                if not member == account:
                    for permission in get_perms(member, pod):
                        permissions_hashmap[permission] += 1

            assigned = False
            for index, permission in enumerate(permissions_list):
                if permissions_hashmap[permission] == 0:
                    for member in pod_members:
                        if index+1 < len(permissions_list) and permissions_list[index+1] in get_perms(member, pod) or \
                           permission == 'add_accounts':
                            assign_perm('change_account_permissions', member, pod)
                            assigned = True
                if assigned:
                    break
            else:
                pod.delete()
        account.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
