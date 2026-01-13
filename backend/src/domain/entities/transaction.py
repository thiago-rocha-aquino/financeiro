from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4


class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


@dataclass
class Transaction:
    """Entidade de domínio que representa uma transação financeira."""

    description: str
    amount: Decimal
    type: TransactionType
    user_id: UUID
    category_id: Optional[UUID] = None
    date: datetime = field(default_factory=datetime.utcnow)
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    notes: Optional[str] = None

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError("O valor da transação não pode ser negativo")

    def update(
        self,
        description: Optional[str] = None,
        amount: Optional[Decimal] = None,
        type: Optional[TransactionType] = None,
        category_id: Optional[UUID] = None,
        date: Optional[datetime] = None,
        notes: Optional[str] = None,
    ) -> None:
        if description:
            self.description = description
        if amount is not None:
            if amount < 0:
                raise ValueError("O valor da transação não pode ser negativo")
            self.amount = amount
        if type:
            self.type = type
        if category_id:
            self.category_id = category_id
        if date:
            self.date = date
        if notes is not None:
            self.notes = notes
        self.updated_at = datetime.utcnow()

    @property
    def is_income(self) -> bool:
        return self.type == TransactionType.INCOME

    @property
    def is_expense(self) -> bool:
        return self.type == TransactionType.EXPENSE

    @property
    def signed_amount(self) -> Decimal:
        """Retorna o valor com sinal (negativo para despesas)."""
        return self.amount if self.is_income else -self.amount
