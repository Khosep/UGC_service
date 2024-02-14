from fastapi import HTTPException, status


class LikeAlreadyExistException(HTTPException):
    def __init__(self, email):
        self.email = email
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
