from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from src.domain.entities import User


class UserRepository(ABC):
    """Interface abstrata para o repositório de usuários."""

    @abstractmethod
    async def create(self, user: User) -> User:
        """Cria um novo usuário."""
        pass

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        """Busca um usuário pelo ID."""
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Busca um usuário pelo email."""
        pass

    @abstractmethod
    async def update(self, user: User) -> User:
        """Atualiza um usuário existente."""
        pass

    @abstractmethod
    async def delete(self, user_id: UUID) -> bool:
        """Remove um usuário."""
        pass
