from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from src.domain.entities import Budget


class BudgetRepository(ABC):
    """Interface abstrata para o repositório de orçamentos."""

    @abstractmethod
    async def create(self, budget: Budget) -> Budget:
        """Cria um novo orçamento."""
        pass

    @abstractmethod
    async def get_by_id(self, budget_id: UUID) -> Optional[Budget]:
        """Busca um orçamento pelo ID."""
        pass

    @abstractmethod
    async def get_by_user_and_period(
        self, user_id: UUID, month: int, year: int
    ) -> list[Budget]:
        """Busca todos os orçamentos de um usuário em um período."""
        pass

    @abstractmethod
    async def get_by_category_and_period(
        self, user_id: UUID, category_id: UUID, month: int, year: int
    ) -> Optional[Budget]:
        """Busca um orçamento específico por categoria e período."""
        pass

    @abstractmethod
    async def update(self, budget: Budget) -> Budget:
        """Atualiza um orçamento existente."""
        pass

    @abstractmethod
    async def delete(self, budget_id: UUID) -> bool:
        """Remove um orçamento."""
        pass
