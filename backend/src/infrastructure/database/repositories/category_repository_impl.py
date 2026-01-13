from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities import Category
from src.domain.repositories import CategoryRepository
from src.infrastructure.database.models import CategoryModel


class CategoryRepositoryImpl(CategoryRepository):
    """Implementação do repositório de categorias com SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _to_entity(self, model: CategoryModel) -> Category:
        return Category(
            id=model.id,
            name=model.name,
            color=model.color,
            icon=model.icon,
            user_id=model.user_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_model(self, entity: Category) -> CategoryModel:
        return CategoryModel(
            id=entity.id,
            name=entity.name,
            color=entity.color,
            icon=entity.icon,
            user_id=entity.user_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    async def create(self, category: Category) -> Category:
        model = self._to_model(category)
        self._session.add(model)
        await self._session.flush()
        return self._to_entity(model)

    async def get_by_id(self, category_id: UUID) -> Optional[Category]:
        result = await self._session.execute(
            select(CategoryModel).where(CategoryModel.id == category_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_all_by_user(self, user_id: UUID) -> list[Category]:
        result = await self._session.execute(
            select(CategoryModel)
            .where(CategoryModel.user_id == user_id)
            .order_by(CategoryModel.name)
        )
        models = result.scalars().all()
        return [self._to_entity(m) for m in models]

    async def update(self, category: Category) -> Category:
        result = await self._session.execute(
            select(CategoryModel).where(CategoryModel.id == category.id)
        )
        model = result.scalar_one_or_none()

        if model:
            model.name = category.name
            model.color = category.color
            model.icon = category.icon
            model.updated_at = category.updated_at
            await self._session.flush()
            return self._to_entity(model)

        raise ValueError("Categoria não encontrada")

    async def delete(self, category_id: UUID) -> bool:
        result = await self._session.execute(
            select(CategoryModel).where(CategoryModel.id == category_id)
        )
        model = result.scalar_one_or_none()

        if model:
            await self._session.delete(model)
            await self._session.flush()
            return True

        return False
