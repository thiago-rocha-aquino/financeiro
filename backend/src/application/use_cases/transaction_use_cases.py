from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from src.application.dtos import (
    TransactionCreateDTO,
    TransactionResponseDTO,
    TransactionUpdateDTO,
)
from src.domain.entities import Transaction, TransactionType
from src.domain.repositories import TransactionRepository


class TransactionSummaryDTO(BaseModel):
    """DTO para resumo de transações."""

    total_income: Decimal
    total_expense: Decimal
    balance: Decimal
    transaction_count: int


class CreateTransactionUseCase:
    """Caso de uso para criação de transação."""

    def __init__(self, transaction_repository: TransactionRepository):
        self._transaction_repository = transaction_repository

    async def execute(
        self, user_id: UUID, dto: TransactionCreateDTO
    ) -> TransactionResponseDTO:
        transaction = Transaction(
            description=dto.description,
            amount=dto.amount,
            type=dto.type,
            user_id=user_id,
            category_id=dto.category_id,
            date=dto.date or datetime.utcnow(),
            notes=dto.notes,
        )

        created_transaction = await self._transaction_repository.create(transaction)
        return TransactionResponseDTO.model_validate(created_transaction)


class GetTransactionsUseCase:
    """Caso de uso para listar transações."""

    def __init__(self, transaction_repository: TransactionRepository):
        self._transaction_repository = transaction_repository

    async def execute(
        self,
        user_id: UUID,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        type: Optional[TransactionType] = None,
        category_id: Optional[UUID] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[TransactionResponseDTO]:
        transactions = await self._transaction_repository.get_all_by_user(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            type=type,
            category_id=category_id,
            limit=limit,
            offset=offset,
        )
        return [TransactionResponseDTO.model_validate(t) for t in transactions]


class UpdateTransactionUseCase:
    """Caso de uso para atualizar transação."""

    def __init__(self, transaction_repository: TransactionRepository):
        self._transaction_repository = transaction_repository

    async def execute(
        self, transaction_id: UUID, user_id: UUID, dto: TransactionUpdateDTO
    ) -> Optional[TransactionResponseDTO]:
        transaction = await self._transaction_repository.get_by_id(transaction_id)

        if not transaction or transaction.user_id != user_id:
            return None

        transaction.update(
            description=dto.description,
            amount=dto.amount,
            type=dto.type,
            category_id=dto.category_id,
            date=dto.date,
            notes=dto.notes,
        )

        updated_transaction = await self._transaction_repository.update(transaction)
        return TransactionResponseDTO.model_validate(updated_transaction)


class DeleteTransactionUseCase:
    """Caso de uso para deletar transação."""

    def __init__(self, transaction_repository: TransactionRepository):
        self._transaction_repository = transaction_repository

    async def execute(self, transaction_id: UUID, user_id: UUID) -> bool:
        transaction = await self._transaction_repository.get_by_id(transaction_id)

        if not transaction or transaction.user_id != user_id:
            return False

        return await self._transaction_repository.delete(transaction_id)


class GetTransactionSummaryUseCase:
    """Caso de uso para obter resumo de transações."""

    def __init__(self, transaction_repository: TransactionRepository):
        self._transaction_repository = transaction_repository

    async def execute(
        self,
        user_id: UUID,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> TransactionSummaryDTO:
        total_income = await self._transaction_repository.get_total_by_type(
            user_id=user_id,
            type=TransactionType.INCOME,
            start_date=start_date,
            end_date=end_date,
        )

        total_expense = await self._transaction_repository.get_total_by_type(
            user_id=user_id,
            type=TransactionType.EXPENSE,
            start_date=start_date,
            end_date=end_date,
        )

        transaction_count = await self._transaction_repository.count_by_user(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
        )

        return TransactionSummaryDTO(
            total_income=total_income,
            total_expense=total_expense,
            balance=total_income - total_expense,
            transaction_count=transaction_count,
        )
