from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities import Budget
from src.domain.repositories import BudgetRepository
from src.infrastructure.database.models import BudgetModel


class BudgetRepositoryImpl(BudgetRepository):
    """Implementação do repositório de orçamentos com SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _to_entity(self, model: BudgetModel) -> Budget:
        return Budget(
            id=model.id,
            user_id=model.user_id,
            category_id=model.category_id,
            amount=model.amount,
            month=model.month,
            year=model.year,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_model(self, entity: Budget) -> BudgetModel:
        return BudgetModel(
            id=entity.id,
            user_id=entity.user_id,
            category_id=entity.category_id,
            amount=entity.amount,
            month=entity.month,
            year=entity.year,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    async def create(self, budget: Budget) -> Budget:
        model = self._to_model(budget)
        self._session.add(model)
        await self._session.flush()
        return self._to_entity(model)

    async def get_by_id(self, budget_id: UUID) -> Optional[Budget]:
        result = await self._session.execute(
            select(BudgetModel).where(BudgetModel.id == budget_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_user_and_period(
        self, user_id: UUID, month: int, year: int
    ) -> list[Budget]:
        result = await self._session.execute(
            select(BudgetModel).where(
                BudgetModel.user_id == user_id,
                BudgetModel.month == month,
                BudgetModel.year == year,
            )
        )
        models = result.scalars().all()
        return [self._to_entity(m) for m in models]

    async def get_by_category_and_period(
        self, user_id: UUID, category_id: UUID, month: int, year: int
    ) -> Optional[Budget]:
        result = await self._session.execute(
            select(BudgetModel).where(
                BudgetModel.user_id == user_id,
                BudgetModel.category_id == category_id,
                BudgetModel.month == month,
                BudgetModel.year == year,
            )
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def update(self, budget: Budget) -> Budget:
        result = await self._session.execute(
            select(BudgetModel).where(BudgetModel.id == budget.id)
        )
        model = result.scalar_one_or_none()

        if model:
            model.amount = budget.amount
            model.updated_at = budget.updated_at
            await self._session.flush()
            return self._to_entity(model)

        raise ValueError("Orçamento não encontrado")

    async def delete(self, budget_id: UUID) -> bool:
        result = await self._session.execute(
            select(BudgetModel).where(BudgetModel.id == budget_id)
        )
        model = result.scalar_one_or_none()

        if model:
            await self._session.delete(model)
            await self._session.flush()
            return True

        return False
