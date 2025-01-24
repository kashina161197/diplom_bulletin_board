from django.urls import path
from rest_framework.routers import DefaultRouter

from announcements.apps import AnnouncementsConfig
from announcements.views import (AnnouncementViewSet, ReviewACreateAPIView,
                                 ReviewDestroyAPIView, ReviewListPIView,
                                 ReviewUpdatePIView)

app_name = AnnouncementsConfig.name


router = DefaultRouter()
router.register(r"announcement", AnnouncementViewSet, basename="announcement")

urlpatterns = [
    path("review_create/", ReviewACreateAPIView.as_view(), name="review_create"),
    path("review/<int:pk>/update", ReviewUpdatePIView.as_view(), name="review_update"),
    path("review_list/", ReviewListPIView.as_view(), name="review_list"),
    path(
        "review/<int:pk>/delete", ReviewDestroyAPIView.as_view(), name="review_delete"
    ),
] + router.urls
