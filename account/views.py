from rest_framework import generics
from account.models import Account
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from account.permissions import IsAdmAccount, IsOwnerAccount
from .serializers import (
    CreateUserAccountManagementSerializer,
    CreateUserAccountSerializer,
)


class ListCreateAccountView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = CreateUserAccountSerializer

    def list_user_from_youngest_to_oldest(self):
        user = self.kwargs["date_joined"]
        return self.queryset.order_by("date_joined")[0:user]


class PatchAccountView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerAccount]
    lookup_url_kwarg = "num"
    queryset = Account.objects.all()
    serializer_class = CreateUserAccountSerializer


class PatchAccountManagementView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdmAccount]
    lookup_url_kwarg = "num"
    queryset = Account.objects.all()
    serializer_class = CreateUserAccountManagementSerializer
