from rest_framework import generics
from product.models import Product
from product.permissions import ProductActivePermissions, ProductPermissions
from product.serializers import ProductSerializerDetailed, ProductSerializerSimple
from rest_framework.authentication import TokenAuthentication
from mixin.mixin import MixinSerializer

# Create your views here.


class ListProductView(MixinSerializer, generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [ProductPermissions]

    queryset = Product.objects.all()
    # serializer_class = ProductSerializerDetailed
    serializers = {
        "POST": ProductSerializerDetailed,
        "GET": ProductSerializerSimple,
    }

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


class TesteView(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [ProductActivePermissions]

    queryset = Product.objects.all()
    serializer_class = ProductSerializerDetailed

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)
