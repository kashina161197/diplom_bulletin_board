from rest_framework import serializers
from .models import CustomsUser, Announcement, Review
from .paginators import ADSPagination


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзыва"""
    class Meta:
        model = Review
        fields = ('id', 'text', 'rating', 'created_at', 'announcement', 'owner')


class AnnouncementSerializer(serializers.ModelSerializer):
    """Сериализатор для объявления"""

    announcement_reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Announcement
        fields = ('id', 'title', 'price', 'description', 'image', 'created_at', 'owner', 'announcement_reviews')

