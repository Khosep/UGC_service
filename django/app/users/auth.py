import http
from enum import Enum
from django.utils import timezone

import requests
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from jose import jwt, JWTError, ExpiredSignatureError

from config.config_django import settings_django

User = get_user_model()


class RightsName(str, Enum):
    """Модель прав доступа в API."""

    admin = "admin"


class CustomBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        url = str(
            f"http://{settings_django.django_auth_api_host}:7005/"
            f"{settings_django.django_auth_api_path}"
        )
        data = {
            "username": username,
            "password": password,
            "grant_type": "",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        }
        headers = {
            "accept": "application / json",
            "Content-type": "application/x-www-form-urlencoded",
            "X-Request-Id": "1",
        }
        response = requests.post(url, data=data, headers=headers)
        if response.status_code == http.HTTPStatus.INTERNAL_SERVER_ERROR:
            user = self.get_user_offline(username, password)
            return user
        if response.status_code != http.HTTPStatus.OK:
            return None

        response_data = response.json()
        try:
            access_token = response_data["access_token"]
            payload = jwt.decode(
                access_token,
                settings_django.django_access_token_secret_key,
                algorithms=settings_django.django_token_jwn_algoritm,
            )
        except ExpiredSignatureError:
            return None
        except JWTError:
            return None
        try:
            user, created = User.objects.get_or_create(
                id=payload["user_id"],
            )
            user.set_password(password)
            user.last_login = timezone.now()
            user.username = payload.get("username")
            user.email = payload.get("email")
            user.is_admin = RightsName.admin in payload.get("roles")
            user.is_staff = RightsName.admin in payload.get("roles")
            user.roles = payload.get("roles")
            user.first_name = payload.get("first_name")
            user.last_name = payload.get("last_name")
            user.is_active = True
            user.save()
            return user
        except Exception:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def get_user_offline(self, username, password):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None
