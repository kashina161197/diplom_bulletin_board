from rest_framework import serializers

from announcements.serializers import AnnouncementSerializer, ReviewSerializer
from .models import CustomsUser


class ProfileUserSerializer(serializers.ModelSerializer):
    """Сериализатор для владельца профиля"""

    announcements = AnnouncementSerializer(many=True, read_only=True)
    author_reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = CustomsUser
        fields = ("id", "email", "password", "first_name", "last_name", "phone", "avatar", "announcements", "author_reviews")


class ProfileOwnerAdSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей, не являющихся владельцами профиля"""

    announcements = AnnouncementSerializer(many=True, read_only=True)
    author_reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = CustomsUser
        fields = ("first_name", "phone", "avatar", "announcements", "author_reviews")


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для админа"""
    class Meta:
        model = CustomsUser
        fields = "__all__"
