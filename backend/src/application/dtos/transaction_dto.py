from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from src.domain.entities import TransactionType


class TransactionCreateDTO(BaseModel):
    """DTO para criação de transação."""

    description: str = Field(..., min_length=1, max_length=200)
    amount: Decimal = Field(..., gt=0, decimal_places=2)
    type: TransactionType
    category_id: Optional[UUID] = None
    date: Optional[datetime] = None
    notes: Optional[str] = Field(None, max_length=500)


class TransactionUpdateDTO(BaseModel):
    """DTO para atualização de transação."""

    description: Optional[str] = Field(None, min_length=1, max_length=200)
    amount: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    type: Optional[TransactionType] = None
    category_id: Optional[UUID] = None
    date: Optional[datetime] = None
    notes: Optional[str] = Field(None, max_length=500)


class TransactionResponseDTO(BaseModel):
    """DTO para resposta de transação."""

    id: UUID
    description: str
    amount: Decimal
    type: TransactionType
    category_id: Optional[UUID]
    user_id: UUID
    date: datetime
    notes: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
