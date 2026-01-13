from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities import User
from src.domain.repositories import UserRepository
from src.infrastructure.database.models import UserModel


class UserRepositoryImpl(UserRepository):
    """Implementação do repositório de usuários com SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _to_entity(self, model: UserModel) -> User:
        return User(
            id=model.id,
            email=model.email,
            name=model.name,
            hashed_password=model.hashed_password,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_model(self, entity: User) -> UserModel:
        return UserModel(
            id=entity.id,
            email=entity.email,
            name=entity.name,
            hashed_password=entity.hashed_password,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    async def create(self, user: User) -> User:
        model = self._to_model(user)
        self._session.add(model)
        await self._session.flush()
        return self._to_entity(model)

    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        result = await self._session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self._session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def update(self, user: User) -> User:
        result = await self._session.execute(
            select(UserModel).where(UserModel.id == user.id)
        )
        model = result.scalar_one_or_none()

        if model:
            model.name = user.name
            model.is_active = user.is_active
            model.updated_at = user.updated_at
            await self._session.flush()
            return self._to_entity(model)

        raise ValueError("Usuário não encontrado")

    async def delete(self, user_id: UUID) -> bool:
        result = await self._session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        model = result.scalar_one_or_none()

        if model:
            await self._session.delete(model)
            await self._session.flush()
            return True

        return False
