from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserCreateDTO(BaseModel):
    """DTO para criação de usuário."""

    email: EmailStr
    name: str = Field(..., min_length=2, max_length=100)
    password: str = Field(..., min_length=8, max_length=100)


class UserUpdateDTO(BaseModel):
    """DTO para atualização de usuário."""

    name: Optional[str] = Field(None, min_length=2, max_length=100)


class UserResponseDTO(BaseModel):
    """DTO para resposta de usuário."""

    id: UUID
    email: str
    name: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
