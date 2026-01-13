from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class User:
    """Entidade de domínio que representa um usuário do sistema."""

    email: str
    name: str
    hashed_password: str
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    is_active: bool = True
    initial_balance: Decimal = Decimal("0")

    def update_name(self, name: str) -> None:
        self.name = name
        self.updated_at = datetime.utcnow()

    def update_initial_balance(self, balance: Decimal) -> None:
        self.initial_balance = balance
        self.updated_at = datetime.utcnow()

    def deactivate(self) -> None:
        self.is_active = False
        self.updated_at = datetime.utcnow()

    def activate(self) -> None:
        self.is_active = True
        self.updated_at = datetime.utcnow()
