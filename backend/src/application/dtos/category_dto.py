from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class CategoryCreateDTO(BaseModel):
    """DTO para criação de categoria."""

    name: str = Field(..., min_length=1, max_length=50)
    color: str = Field(default="#6366f1", pattern=r"^#[0-9A-Fa-f]{6}$")
    icon: str = Field(default="tag", max_length=30)


class CategoryUpdateDTO(BaseModel):
    """DTO para atualização de categoria."""

    name: Optional[str] = Field(None, min_length=1, max_length=50)
    color: Optional[str] = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")
    icon: Optional[str] = Field(None, max_length=30)


class CategoryResponseDTO(BaseModel):
    """DTO para resposta de categoria."""

    id: UUID
    name: str
    color: str
    icon: str
    user_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
