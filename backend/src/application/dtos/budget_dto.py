from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class BudgetCreateDTO(BaseModel):
    """DTO para criação de orçamento."""

    category_id: UUID
    amount: Decimal = Field(..., gt=0, decimal_places=2)
    month: int = Field(..., ge=1, le=12)
    year: int = Field(..., ge=2000)


class BudgetUpdateDTO(BaseModel):
    """DTO para atualização de orçamento."""

    amount: Optional[Decimal] = Field(None, gt=0, decimal_places=2)


class BudgetResponseDTO(BaseModel):
    """DTO para resposta de orçamento."""

    id: UUID
    user_id: UUID
    category_id: UUID
    amount: Decimal
    month: int
    year: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    spent: Optional[Decimal] = None
    remaining: Optional[Decimal] = None
    percentage_used: Optional[float] = None

    model_config = {"from_attributes": True}
