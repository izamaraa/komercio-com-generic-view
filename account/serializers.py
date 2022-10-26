from rest_framework import serializers

from .models import Account


class CreateUserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "password",
            "is_seller",
            "date_joined",
            "is_superuser",
            "is_active",
        ]
        read_only_fields = [
            "id",
            "date_joined",
            "is_superuser",
            "is_active",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):

        resultado = Account.objects.create_user(**validated_data)

        return resultado


class CreateUserAccountManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["is_active"]
