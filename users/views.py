
from rest_framework.generics import CreateAPIView
from django.core.mail import send_mail
from users.models import CustomsUser
from users.serializers import UserSerializer

import secrets

from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from config.settings import EMAIL_HOST_USER



class UserCreateAPIView(CreateAPIView):

    """Контроллер для создание пользователя"""

    serializer_class = UserSerializer
    queryset = CustomsUser.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        """Подтверждение почты"""
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

    def get(self, token):
        """Подтверждение email-адреса пользователя"""
        user = get_object_or_404(CustomsUser, token=token)
        user.is_active = True
        user.save(update_fields=["is_active"])
        return Response({"message": "Ваша учетная запись подтверждена!"}, status=status.HTTP_200_OK)


class UserProfileViewSet(viewsets.ModelViewSet):

    """Контроллер просмотра профиля пользотеля"""

    queryset = CustomsUser.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return self.queryset.filter(id=self.request.user.id)

    def perform_update(self, serializer):
        serializer.save()
