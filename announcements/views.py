from rest_framework import generics, viewsets

from announcements.models import Announcement, Review
from announcements.paginators import ADSPagination
from announcements.serializers import AnnouncementSerializer, ReviewSerializer


class AnnouncementViewSet(viewsets.ModelViewSet):
    """CRUD объявлений."""

    queryset = Announcement.objects.all()
    pagination_class = ADSPagination
    serializer_class = AnnouncementSerializer
    # permission_classes = [IsOwner, IsAuthenticated]

    def perform_create(self, serializer):
        announcement = serializer.save()
        announcement.owner = self.request.user
        announcement.save()


class ReviewACreateAPIView(generics.CreateAPIView):
    """Создание отзыва."""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [~IsModer, IsAuthenticated]

    def perform_create(self, serializer):
        review = serializer.save()
        review.owner = self.request.user
        review.save()


class ReviewListAPIView(generics.ListAPIView):
    """Просмотр отзывов."""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = ADSPagination


class ReviewDestroyAPIView(generics.DestroyAPIView):
    """Удаление отзыва."""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = (IsAuthenticated, IsOwner | ~IsModer)
