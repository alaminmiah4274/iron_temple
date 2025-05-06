from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers


# TO CREATE USER
class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
            "address",
            "phone_number",
        ]


# TO SHOW CURRENT USER INFO
class GetCurrentUserSerializer(UserSerializer):
    role = serializers.SerializerMethodField(method_name="get_role")

    class Meta(UserSerializer.Meta):
        ref_name = "CustomUser"
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "address",
            "phone_number",
            "is_staff",
            "role",
        ]
        read_only_fields = ["is_staff"]

    def get_role(self, obj):
        if obj.is_superuser:
            return "admin"
        elif obj.is_staff:
            return "staff"
        return "user"
