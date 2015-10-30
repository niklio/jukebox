from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404

from rest_framework import permissions, viewsets, status
from rest_framework.response import Response

from rest_framework_jwt.views import api_settings

from authentication.models import Account
from authentication.permissions import IsAccountOwner
from authentication.serializers import AccountSerializer
from pods.models import Pod


class AccountViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    lookup_field = 'username'
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)

        if self.request.method == 'POST':
            return (permissions.AllowAny(),)

        return (permissions.IsAuthenticated(), IsAccountOwner())


    def list(self, request, pod_name=None):
        queryset = self.queryset
        
        if pod_name:
            pod = Pod.objects.get(name=pod_name)
            queryset = queryset.filter(pod=pod)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            account = Account.objects.create_user(**serializer.validated_data)

            return Response(
                serializer.validated_data,
                status=status.HTTP_201_CREATED,
                headers={'Location': '/api/accounts/{0}'.format(serializer.validated_data['username'])}
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
