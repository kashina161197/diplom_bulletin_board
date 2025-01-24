from django.urls import include, path
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.apps import UsersConfig
from users.views import (EmailConfirmAPIView, PasswordResetAPIView,
                         PasswordResetConfirmAPIView, UserCreateAPIView,
                         UserProfileViewSet)

app_name = UsersConfig.name


router = DefaultRouter()
router.register(r"profile", UserProfileViewSet, basename="user-profile")

urlpatterns = [
    path(
        "email-confirm/<str:token>",
        EmailConfirmAPIView.as_view(permission_classes=(AllowAny,)),
        name="email_confirm",
    ),
    path("", include(router.urls)),
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="token_obtain_pair",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path("reset_password/", PasswordResetAPIView.as_view(), name="reset_password"),
    path(
        "reset_password_confirm/<uid>/<token>/",
        PasswordResetConfirmAPIView.as_view(),
        name="reset_password_confirm",
    ),
]
