from pydantic import BaseModel, EmailStr


class LoginDTO(BaseModel):
    """DTO para login."""

    email: EmailStr
    password: str


class TokenDTO(BaseModel):
    """DTO para token de autenticação."""

    access_token: str
    token_type: str = "bearer"
