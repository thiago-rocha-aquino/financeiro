from abc import ABC, abstractmethod
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from src.domain.entities import Transaction, TransactionType


class TransactionRepository(ABC):
    """Interface abstrata para o repositório de transações."""

    @abstractmethod
    async def create(self, transaction: Transaction) -> Transaction:
        """Cria uma nova transação."""
        pass

    @abstractmethod
    async def get_by_id(self, transaction_id: UUID) -> Optional[Transaction]:
        """Busca uma transação pelo ID."""
        pass

    @abstractmethod
    async def get_all_by_user(
        self,
        user_id: UUID,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        type: Optional[TransactionType] = None,
        category_id: Optional[UUID] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Transaction]:
        """Busca todas as transações de um usuário com filtros opcionais."""
        pass

    @abstractmethod
    async def get_total_by_type(
        self,
        user_id: UUID,
        type: TransactionType,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Decimal:
        """Calcula o total de transações por tipo."""
        pass

    @abstractmethod
    async def get_total_by_category(
        self,
        user_id: UUID,
        category_id: UUID,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Decimal:
        """Calcula o total de transações por categoria."""
        pass

    @abstractmethod
    async def update(self, transaction: Transaction) -> Transaction:
        """Atualiza uma transação existente."""
        pass

    @abstractmethod
    async def delete(self, transaction_id: UUID) -> bool:
        """Remove uma transação."""
        pass

    @abstractmethod
    async def count_by_user(
        self,
        user_id: UUID,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> int:
        """Conta o número de transações de um usuário."""
        pass
