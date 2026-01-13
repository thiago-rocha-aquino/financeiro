from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class Budget:
    """Entidade de domínio que representa um orçamento mensal."""

    user_id: UUID
    category_id: UUID
    amount: Decimal
    month: int
    year: int
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError("O valor do orçamento não pode ser negativo")
        if not 1 <= self.month <= 12:
            raise ValueError("Mês deve estar entre 1 e 12")
        if self.year < 2000:
            raise ValueError("Ano inválido")

    def update_amount(self, amount: Decimal) -> None:
        if amount < 0:
            raise ValueError("O valor do orçamento não pode ser negativo")
        self.amount = amount
        self.updated_at = datetime.utcnow()

    def calculate_remaining(self, spent: Decimal) -> Decimal:
        """Calcula o valor restante do orçamento."""
        return self.amount - spent

    def calculate_percentage_used(self, spent: Decimal) -> float:
        """Calcula a porcentagem utilizada do orçamento."""
        if self.amount == 0:
            return 0.0
        return float((spent / self.amount) * 100)

    def is_exceeded(self, spent: Decimal) -> bool:
        """Verifica se o orçamento foi excedido."""
        return spent > self.amount
