from rest_framework import serializers
from rest_framework.authtoken.admin import User


class SignupSerializer(serializers.ModelSerializer):
    """
    info: serializer for registering the USER,
    model: rest_framework.authtoken.admin.User
    selected_fields = username , password
    write_only fields = password
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data["password"]  # saves password in hashes
        )
        return user
