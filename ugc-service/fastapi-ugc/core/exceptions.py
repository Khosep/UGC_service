from fastapi import HTTPException, status


class TooManyRequestsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Превышен лимит запросов",
        )


class ValidationException(HTTPException):
    def __init__(self, item):
        self.item = item
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid {self.item}",
        )


class TokenExpiredException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Срок действия токена истек",
        )


class CredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
