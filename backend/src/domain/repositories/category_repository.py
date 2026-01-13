from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from src.domain.entities import Category


class CategoryRepository(ABC):
    """Interface abstrata para o repositório de categorias."""

    @abstractmethod
    async def create(self, category: Category) -> Category:
        """Cria uma nova categoria."""
        pass

    @abstractmethod
    async def get_by_id(self, category_id: UUID) -> Optional[Category]:
        """Busca uma categoria pelo ID."""
        pass

    @abstractmethod
    async def get_all_by_user(self, user_id: UUID) -> list[Category]:
        """Busca todas as categorias de um usuário."""
        pass

    @abstractmethod
    async def update(self, category: Category) -> Category:
        """Atualiza uma categoria existente."""
        pass

    @abstractmethod
    async def delete(self, category_id: UUID) -> bool:
        """Remove uma categoria."""
        pass
