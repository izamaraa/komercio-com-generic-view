from rest_framework import serializers
from account.serializers import CreateUserAccountSerializer

from product.models import Product


class ProductSerializerDetailed(serializers.ModelSerializer):
    seller = CreateUserAccountSerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "seller",
            "description",
            "price",
            "quantity",
            "is_active",
        ]
        read_only_fields = ["id", "is_active"]
        depth = 1


class ProductSerializerSimple(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "description",
            "price",
            "quantity",
            "is_active",
            "seller_id",
        ]
