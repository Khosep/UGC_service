from functools import lru_cache

from jose import jwt, JWTError, ExpiredSignatureError
from pydantic import ValidationError

from core.config import settings
from core.exceptions import (
    CredentialsException,
    TokenExpiredException,
    ValidationException,
)
from schemas.token_schema import Token


class TokenService:
    def get_token_data(self, token: str) -> Token:
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
            token_data = Token(
                user_id=payload.get("user_id"),
                username=payload.get("username"),
                roles=payload.get("roles"),
                email=payload.get("email"),
                first_name=payload.get("first_name"),
                last_name=payload.get("last_name"),
            )
            return token_data
        except ExpiredSignatureError as exc:
            raise TokenExpiredException from exc
        except (JWTError, ValidationError) as exc:
            raise ValidationException("access_token") from exc

    def extract_token(self, authorization: str | None = None) -> str | None:
        if authorization is None:
            return None
        if not authorization.startswith("Bearer "):
            raise CredentialsException
        return authorization.split(" ")[1]


@lru_cache()
def get_token_service() -> TokenService:
    return TokenService()
