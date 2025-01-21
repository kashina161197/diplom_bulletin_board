from rest_framework import generics, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from users.permissions import IsModer, IsOwner
from announcements.filters import AnnouncementFilter
from announcements.models import Announcement, Review
from announcements.paginators import ADSPagination
from announcements.serializers import AnnouncementSerializer, ReviewSerializer, AnnouncementRetrieveSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny


class AnnouncementViewSet(viewsets.ModelViewSet):
    """CRUD объявлений."""

    queryset = Announcement.objects.all()
    pagination_class = ADSPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = AnnouncementFilter
    filterset_fields = ("owner", "title", "created_at",)
    search_fields = ("title",)
    ordering_fields = ("created_at",)

    def perform_create(self, serializer):
        announcement = serializer.save()
        announcement.owner = self.request.user
        announcement.save()

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия."""
        if self.action == 'retrieve':
            return AnnouncementRetrieveSerializer
        return AnnouncementSerializer

    def get_permissions(self):
        if self.action == "list":
            self.permission_classes = [AllowAny]
        elif self.action == "create":
            self.permission_classes = [IsAuthenticated]
        elif self.action in "retrieve":
            self.permission_classes = [IsAuthenticated | IsModer | IsOwner]
        elif self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = [IsOwner | IsModer]

        return super().get_permissions()


class ReviewACreateAPIView(generics.CreateAPIView):
    """Создание отзыва."""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        review = serializer.save()
        review.owner = self.request.user
        review.save()


class ReviewListPIView(generics.ListAPIView):
    """Список отзывов."""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = ADSPagination
    permission_classes = [AllowAny]


class ReviewUpdatePIView(generics.UpdateAPIView):
    """Редактирование отзыва."""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsModer]


class ReviewDestroyAPIView(generics.DestroyAPIView):
    """Удаление отзыва."""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsModer]
