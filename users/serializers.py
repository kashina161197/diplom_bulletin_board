from rest_framework import serializers

from announcements.models import Review
from announcements.paginators import ADSPagination
from announcements.serializers import AnnouncementSerializer, ReviewSerializer

from .models import CustomsUser


class CreateUserSerializer(serializers.ModelSerializer):
    """Сериализатор для создания профиля"""

    class Meta:
        model = CustomsUser
        fields = "__all__"


class ProfileUserSerializer(serializers.ModelSerializer):
    """Сериализатор для владельца профиля"""

    announcements = AnnouncementSerializer(many=True, read_only=True)
    author_reviews = ReviewSerializer(many=True, read_only=True)
    received_reviews = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = CustomsUser
        fields = (
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "phone_number",
            "avatar",
            "announcements",
            "author_reviews",
            "received_reviews",
            "average_rating",
        )

    def get_received_reviews(self, obj):
        """Получаем оставленные отзывы"""
        announcements = obj.announcements.all()
        reviews = Review.objects.filter(announcement__in=announcements)

        paginator = ADSPagination()
        paginated_reviews = paginator.paginate_queryset(
            reviews, self.context["request"]
        )

        return ReviewSerializer(paginated_reviews, many=True).data

    def get_average_rating(self, obj):
        """Получаем общий рейтинг"""
        announcements = obj.announcements.all()
        reviews = Review.objects.filter(announcement__in=announcements)

        if reviews.exists():
            total_rating = sum(review.rating for review in reviews)
            average_rating = total_rating / reviews.count()
            return round(average_rating, 2)
        return 0


class ProfileOwnerAdSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей, не являющихся владельцами профиля"""

    announcements = AnnouncementSerializer(many=True, read_only=True)
    reviews = serializers.SerializerMethodField()
    overall_rating = serializers.SerializerMethodField()

    class Meta:
        model = CustomsUser
        fields = (
            "first_name",
            "phone_number",
            "avatar",
            "announcements",
            "reviews",
            "overall_rating",
        )

    def get_reviews(self, obj):
        """Получаем оставленные отзывы"""
        announcements = obj.announcements.all()
        reviews = Review.objects.filter(announcement__in=announcements)

        paginator = ADSPagination()
        paginated_reviews = paginator.paginate_queryset(
            reviews, self.context["request"]
        )
        return ReviewSerializer(paginated_reviews, many=True).data

    def get_overall_rating(self, obj):
        """Получаем общий рейтинг"""
        announcements = obj.announcements.all()
        reviews = Review.objects.filter(announcement__in=announcements)

        if reviews.exists():
            total_rating = sum(review.rating for review in reviews)
            average_rating = total_rating / reviews.count()
            return round(average_rating, 2)
        return 0
