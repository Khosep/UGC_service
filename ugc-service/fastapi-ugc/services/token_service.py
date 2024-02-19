from functools import lru_cache

from jose import jwt, JWTError, ExpiredSignatureError
from pydantic import ValidationError

from core.config import settings
from core.exceptions import CredentialsException, TokenExpiredException, ValidationException


class TokenService:

    def get_user_id(self, token: str):
        """Получаем токен из декодированного токена."""
        payload = self.get_payload(token)
        return payload.get("user_id")

    def get_payload(self, token: str) -> dict:
        """Декодируем токен."""
        try:
            payload = jwt.decode(
                token,
                key=settings.access_token_secret_key,
                algorithms=settings.token_jwt_algorithm,
            )
            user_id = payload.get("user_id")
            if user_id is None:
                raise CredentialsException
            return payload
        except ExpiredSignatureError as exc:
            raise TokenExpiredException from exc
        except (JWTError, ValidationError) as exc:
            raise ValidationException("access_token") from exc


@lru_cache()
def get_token_service() -> TokenService:
    return TokenService()
