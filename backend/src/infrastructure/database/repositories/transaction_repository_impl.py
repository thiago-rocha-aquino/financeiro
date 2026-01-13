from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities import Transaction, TransactionType
from src.domain.repositories import TransactionRepository
from src.infrastructure.database.models import TransactionModel


class TransactionRepositoryImpl(TransactionRepository):
    """Implementação do repositório de transações com SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _to_entity(self, model: TransactionModel) -> Transaction:
        return Transaction(
            id=model.id,
            description=model.description,
            amount=model.amount,
            type=model.type,
            date=model.date,
            notes=model.notes,
            user_id=model.user_id,
            category_id=model.category_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_model(self, entity: Transaction) -> TransactionModel:
        return TransactionModel(
            id=entity.id,
            description=entity.description,
            amount=entity.amount,
            type=entity.type,
            date=entity.date,
            notes=entity.notes,
            user_id=entity.user_id,
            category_id=entity.category_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    async def create(self, transaction: Transaction) -> Transaction:
        model = self._to_model(transaction)
        self._session.add(model)
        await self._session.flush()
        return self._to_entity(model)

    async def get_by_id(self, transaction_id: UUID) -> Optional[Transaction]:
        result = await self._session.execute(
            select(TransactionModel).where(TransactionModel.id == transaction_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

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
        query = select(TransactionModel).where(TransactionModel.user_id == user_id)

        if start_date:
            query = query.where(TransactionModel.date >= start_date)
        if end_date:
            query = query.where(TransactionModel.date < end_date)
        if type:
            query = query.where(TransactionModel.type == type)
        if category_id:
            query = query.where(TransactionModel.category_id == category_id)

        query = query.order_by(TransactionModel.date.desc()).limit(limit).offset(offset)

        result = await self._session.execute(query)
        models = result.scalars().all()
        return [self._to_entity(m) for m in models]

    async def get_total_by_type(
        self,
        user_id: UUID,
        type: TransactionType,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Decimal:
        query = select(func.coalesce(func.sum(TransactionModel.amount), 0)).where(
            TransactionModel.user_id == user_id,
            TransactionModel.type == type,
        )

        if start_date:
            query = query.where(TransactionModel.date >= start_date)
        if end_date:
            query = query.where(TransactionModel.date <= end_date)

        result = await self._session.execute(query)
        total = result.scalar()
        return Decimal(str(total)) if total else Decimal("0")

    async def get_total_by_category(
        self,
        user_id: UUID,
        category_id: UUID,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Decimal:
        query = select(func.coalesce(func.sum(TransactionModel.amount), 0)).where(
            TransactionModel.user_id == user_id,
            TransactionModel.category_id == category_id,
            TransactionModel.type == TransactionType.EXPENSE,
        )

        if start_date:
            query = query.where(TransactionModel.date >= start_date)
        if end_date:
            query = query.where(TransactionModel.date < end_date)

        result = await self._session.execute(query)
        total = result.scalar()
        return Decimal(str(total)) if total else Decimal("0")

    async def update(self, transaction: Transaction) -> Transaction:
        result = await self._session.execute(
            select(TransactionModel).where(TransactionModel.id == transaction.id)
        )
        model = result.scalar_one_or_none()

        if model:
            model.description = transaction.description
            model.amount = transaction.amount
            model.type = transaction.type
            model.date = transaction.date
            model.notes = transaction.notes
            model.category_id = transaction.category_id
            model.updated_at = transaction.updated_at
            await self._session.flush()
            return self._to_entity(model)

        raise ValueError("Transação não encontrada")

    async def delete(self, transaction_id: UUID) -> bool:
        result = await self._session.execute(
            select(TransactionModel).where(TransactionModel.id == transaction_id)
        )
        model = result.scalar_one_or_none()

        if model:
            await self._session.delete(model)
            await self._session.flush()
            return True

        return False

    async def count_by_user(
        self,
        user_id: UUID,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> int:
        query = select(func.count(TransactionModel.id)).where(
            TransactionModel.user_id == user_id
        )

        if start_date:
            query = query.where(TransactionModel.date >= start_date)
        if end_date:
            query = query.where(TransactionModel.date < end_date)

        result = await self._session.execute(query)
        return result.scalar() or 0
