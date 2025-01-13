from django.urls import include, path
from rest_framework.permissions import AllowAny


from announcements.apps import AnnouncementsConfig
from users.views import UserCreateAPIView, UserProfileViewSet, EmailConfirmAPIView, PasswordResetAPIView, PasswordResetConfirmAPIView

app_name = AnnouncementsConfig.name



urlpatterns = [
    # path("email-confirm/<str:token>", EmailConfirmAPIView.as_view(permission_classes=(AllowAny,)), name="email_confirm"),
    # path("reset_password_confirm/<uid>/<token>/", PasswordResetConfirmAPIView.as_view(), name="reset_password_confirm")
]
