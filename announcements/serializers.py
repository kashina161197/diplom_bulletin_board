from rest_framework import serializers
from .models import CustomsUser, Announcement, Review


class AnnouncementSerializer(serializers.ModelSerializer):
    """Сериализатор для объявления"""
    class Meta:
        model = Announcement
        fields = ('id', 'title', 'price', 'description', 'image', 'created_at', 'owner')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзыва"""
    class Meta:
        model = Review
        fields = ('id', 'text', 'rating', 'created_at', 'announcement', 'owner')
