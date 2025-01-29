import pytest
from rest_framework.test import APIClient

from users.models import CustomsUser


@pytest.fixture
def api_client():
    """
    Клиент для тестирования API
    """
    return APIClient()


@pytest.fixture
def user_is_owner_fixture():
    """
    фикстура модели User
    """
    user = CustomsUser.objects.create(
        email="test@test.ru", password="Qwerty", is_active=True
    )
    return user


@pytest.fixture
def user_fixture():
    """
    фикстура модели User без авторизации
    """
    user = CustomsUser.objects.create(
        email="test1@test.ru", password="Qwerty", is_active=True, token="123test"
    )
    return user


@pytest.fixture
def admin_fixture():
    """
    фикстура модели Admin
    """
    user = CustomsUser.objects.create(
        email="admin@test.ru", password="Qwerty", is_active=True, is_staff=True
    )
    return user
