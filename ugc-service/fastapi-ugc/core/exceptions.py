from fastapi import HTTPException, status


class LikeAlreadyExistException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Вы уже поставили лайк этому фильму ранее.",
        )


class TooManyRequestsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Превышен лимит запросов",
        )


class ReviewAlreadyExistException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Вы уже оставили отзыв к этому фильму ранее.",
        )


class ReviewANotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Отзыв не найден",
        )


class ReviewIdentificatorNotExistException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Предоставьте ID фильма и/или ID пользователя.",
        )
