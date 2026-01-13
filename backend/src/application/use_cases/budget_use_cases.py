from datetime import datetime
from typing import Optional
from uuid import UUID

from src.application.dtos import BudgetCreateDTO, BudgetResponseDTO, BudgetUpdateDTO
from src.domain.entities import Budget, TransactionType
from src.domain.repositories import BudgetRepository, TransactionRepository


class CreateBudgetUseCase:
    """Caso de uso para criação de orçamento."""

    def __init__(self, budget_repository: BudgetRepository):
        self._budget_repository = budget_repository

    async def execute(self, user_id: UUID, dto: BudgetCreateDTO) -> BudgetResponseDTO:
        existing = await self._budget_repository.get_by_category_and_period(
            user_id=user_id,
            category_id=dto.category_id,
            month=dto.month,
            year=dto.year,
        )

        if existing:
            raise ValueError("Já existe um orçamento para esta categoria neste período")

        budget = Budget(
            user_id=user_id,
            category_id=dto.category_id,
            amount=dto.amount,
            month=dto.month,
            year=dto.year,
        )

        created_budget = await self._budget_repository.create(budget)
        return BudgetResponseDTO.model_validate(created_budget)


class GetBudgetsUseCase:
    """Caso de uso para listar orçamentos com gastos."""

    def __init__(
        self,
        budget_repository: BudgetRepository,
        transaction_repository: TransactionRepository,
    ):
        self._budget_repository = budget_repository
        self._transaction_repository = transaction_repository

    async def execute(
        self, user_id: UUID, month: int, year: int
    ) -> list[BudgetResponseDTO]:
        budgets = await self._budget_repository.get_by_user_and_period(
            user_id=user_id, month=month, year=year
        )

        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)

        results = []
        for budget in budgets:
            spent = await self._transaction_repository.get_total_by_category(
                user_id=user_id,
                category_id=budget.category_id,
                start_date=start_date,
                end_date=end_date,
            )

            budget_dto = BudgetResponseDTO.model_validate(budget)
            budget_dto.spent = spent
            budget_dto.remaining = budget.calculate_remaining(spent)
            budget_dto.percentage_used = budget.calculate_percentage_used(spent)
            results.append(budget_dto)

        return results


class UpdateBudgetUseCase:
    """Caso de uso para atualizar orçamento."""

    def __init__(self, budget_repository: BudgetRepository):
        self._budget_repository = budget_repository

    async def execute(
        self, budget_id: UUID, user_id: UUID, dto: BudgetUpdateDTO
    ) -> Optional[BudgetResponseDTO]:
        budget = await self._budget_repository.get_by_id(budget_id)

        if not budget or budget.user_id != user_id:
            return None

        if dto.amount:
            budget.update_amount(dto.amount)

        updated_budget = await self._budget_repository.update(budget)
        return BudgetResponseDTO.model_validate(updated_budget)


class DeleteBudgetUseCase:
    """Caso de uso para deletar orçamento."""

    def __init__(self, budget_repository: BudgetRepository):
        self._budget_repository = budget_repository

    async def execute(self, budget_id: UUID, user_id: UUID) -> bool:
        budget = await self._budget_repository.get_by_id(budget_id)

        if not budget or budget.user_id != user_id:
            return False

        return await self._budget_repository.delete(budget_id)
