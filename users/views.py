import secrets

from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from announcements.paginators import ADSPagination
from config.settings import EMAIL_HOST_USER
from users.models import CustomsUser
from users.permissions import IsModer, IsUser
from users.serializers import (CreateUserSerializer, ProfileOwnerAdSerializer,
                               ProfileUserSerializer)


@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_description="Представление создания пользователя"
    ),
)
class UserCreateAPIView(CreateAPIView):
    """Контроллер для создание пользователя"""

    serializer_class = CreateUserSerializer
    queryset = CustomsUser.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        """Создание пользователя и активация УЗ"""

        user = serializer.save()
        user.is_active = False
        user.set_password(user.password)
        token = secrets.token_hex(16)
        user.token = token
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}"
        user.save(update_fields=["token", "is_active", "password"])
        send_mail(
            subject="Активация учетной записи",
            message=f"Для активации учетной записи пройдите по ссылке {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )


class EmailConfirmAPIView(APIView):
    """Представление для подтверждения email-адреса пользователя"""

    def get(self, request, token):
        """Подтверждение email-адреса пользователя"""

        user = get_object_or_404(CustomsUser, token=token)
        user.is_active = True
        user.save(update_fields=["is_active"])
        return Response(
            {"message": "Ваша учетная запись подтверждена!"}, status=status.HTTP_200_OK
        )


class PasswordResetAPIView(APIView):
    """Контроллер для сброса пароля"""

    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response(
                {"error": "Требуется электронная почта."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = CustomsUser.objects.get(email=email)
        except ObjectDoesNotExist:
            return Response(
                {
                    "error": "Пользователь с таким адресом электронной почты не существует."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        uid = user.pk
        token = user.token
        host = self.request.get_host()

        reset_link = f"http://{host}/users/reset_password_confirm/{uid}/{token}/"

        send_mail(
            subject="Сброс пароля",
            message=f"Для сброса пароля перейдите по следующей ссылке: {reset_link}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )

        return Response(
            {"message": "Ссылка для сброса пароля отправлена на ваш email."},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmAPIView(APIView):
    """Контроллер для подтверждения сброса пароля"""

    permission_classes = [AllowAny]

    def post(self, request, uid, token):
        password = request.data.get("password")
        if not password:
            return Response(
                {"error": "Требуется ввести пароль."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = get_object_or_404(CustomsUser, pk=uid)

        if user is not None and user.token == token:
            user.set_password(password)
            user.token = secrets.token_hex(16)
            user.save()
            return Response(
                {"message": "Пароль успешно изменен."}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "Ссылка для сброса пароля недействительна."},
                status=status.HTTP_400_BAD_REQUEST,
            )


@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_description="Представление просмотра конкретного пользователя"
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        operation_description="Представление изменения пользователя"
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        operation_description="Представление частичного изменения пользователя"
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        operation_description="Представление удаления пользователя"
    ),
)
class UserProfileViewSet(viewsets.ModelViewSet):
    """Контроллер просмотра профиля пользователя"""

    queryset = CustomsUser.objects.all()
    pagination_class = ADSPagination

    def get_permissions(self):
        if self.action == "retrieve":
            self.permission_classes = [AllowAny]
        if self.action in ("update", "partial_update", "destroy"):
            self.permission_classes = (IsUser | IsModer,)
        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return ProfileUserSerializer
        if self.request.user.id == self.get_object().id:
            return ProfileUserSerializer
        return ProfileOwnerAdSerializer

    def get_queryset(self):
        return CustomsUser.objects.all()

    def perform_update(self, serializer):
        serializer.save()
