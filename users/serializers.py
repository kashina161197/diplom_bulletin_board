from rest_framework import serializers

from .models import CustomsUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomsUser
        fields = ("id", "email", "password", "first_name", "last_name", "phone", "avatar")
