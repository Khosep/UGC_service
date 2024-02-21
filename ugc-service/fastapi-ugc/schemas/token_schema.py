from pydantic import BaseModel


class Token(BaseModel):
    user_id: str
    username: str
    roles: list[str]
    email: str
    first_name: str
    last_name: str
