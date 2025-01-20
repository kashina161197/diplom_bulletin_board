
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView

from announcements.paginators import ADSPagination
from users.models import CustomsUser
from users.permissions import IsOwner, IsModer
from users.serializers import ProfileUserSerializer, UserSerializer, ProfileOwnerAdSerializer
from rest_framework.response import Response
import secrets
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from django.core.exceptions import ObjectDoesNotExist
from config.settings import EMAIL_HOST_USER


class UserCreateAPIView(CreateAPIView):

    """Контроллер для создание пользователя"""

    serializer_class = ProfileUserSerializer
    queryset = CustomsUser.objects.all()
    permission_classes = (AllowAny,)

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
        return Response({"message": "Ваша учетная запись подтверждена!"}, status=status.HTTP_200_OK)


class PasswordResetAPIView(APIView):
    """Контроллер для сброса пароля"""

    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Требуется электронная почта."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomsUser.objects.get(email=email)
        except ObjectDoesNotExist:
            return Response({"error": "Пользователь с таким адресом электронной почты не существует."},
                            status=status.HTTP_404_NOT_FOUND)

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

        return Response({"message": "Ссылка для сброса пароля отправлена на ваш email."}, status=status.HTTP_200_OK)


class PasswordResetConfirmAPIView(APIView):
    """Контроллер для подтверждения сброса пароля"""

    permission_classes = [AllowAny]

    def post(self, request, uid):
        password = request.data.get("password")
        if not password:
            return Response({"error": "Требуется ввести пароль."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            uid = uid
            user = CustomsUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, ObjectDoesNotExist):
            user = None

        if user is not None and user.token:
            user.set_password(password)
            user.token = secrets.token_hex(16)
            user.save()
            return Response({"message": "Пароль успешно изменен."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Ссылка для сброса пароля недействительна."}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(viewsets.ModelViewSet):
    """Контроллер просмотра профиля пользователя"""

    queryset = CustomsUser .objects.all()
    pagination_class = ADSPagination

    def get_permissions(self):
        if self.action in ("update", "destroy"):
            self.permission_classes = (IsOwner | IsModer,)
        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return UserSerializer
        if self.request.user.id == self.get_object().id:
            return ProfileUserSerializer
        return ProfileOwnerAdSerializer

    def get_queryset(self):
        return CustomsUser.objects.all()

    def perform_update(self, serializer):
        serializer.save()

