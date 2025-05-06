from djoser.serializers import UserCreateSerializer, UserSerializer


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
        ]
        read_only_fields = ["is_staff"]
