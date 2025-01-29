from rest_framework import serializers

from .models import Announcement, Review
from .validators.validators import (ForbiddenWordValidator,
                                    RepeatAnnouncementValidator,
                                    price_zero_validator)


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзыва"""

    class Meta:
        model = Review
        fields = ("id", "text", "rating", "created_at", "announcement", "owner")
        validators = [ForbiddenWordValidator(review_text="text")]


class AnnouncementSerializer(serializers.ModelSerializer):
    """Сериализатор для объявления"""

    price = serializers.IntegerField(validators=(price_zero_validator,))
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Announcement
        fields = (
            "id",
            "title",
            "price",
            "description",
            "image",
            "created_at",
            "owner",
            "average_rating",
        )
        validators = [
            ForbiddenWordValidator(
                announcement_title="title", announcement_description="description"
            ),
            RepeatAnnouncementValidator(
                title="title", description="description", price="price"
            ),
        ]

    def get_average_rating(self, obj):
        """Получаем общий рейтинг для данного объявления"""
        reviews = obj.announcement_reviews.all()

        if reviews.exists():
            total_rating = sum(review.rating for review in reviews)
            average_rating = total_rating / reviews.count()
            return round(average_rating, 2)
        return 0


class AnnouncementRetrieveSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра одного объявления"""

    announcement_reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Announcement
        fields = (
            "id",
            "title",
            "price",
            "description",
            "image",
            "created_at",
            "owner",
            "announcement_reviews",
        )
