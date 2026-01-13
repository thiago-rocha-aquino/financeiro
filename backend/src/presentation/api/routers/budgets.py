from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.application.dtos import BudgetCreateDTO, BudgetResponseDTO, BudgetUpdateDTO
from src.application.use_cases import (
    CreateBudgetUseCase,
    DeleteBudgetUseCase,
    GetBudgetsUseCase,
    UpdateBudgetUseCase,
)
from src.infrastructure.database.repositories import BudgetRepositoryImpl, TransactionRepositoryImpl
from src.presentation.api.dependencies import (
    CurrentUser,
    get_budget_repository,
    get_transaction_repository,
)

router = APIRouter(prefix="/budgets", tags=["Orçamentos"])


@router.post("/", response_model=BudgetResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_budget(
    dto: BudgetCreateDTO,
    current_user: CurrentUser,
    budget_repository: Annotated[BudgetRepositoryImpl, Depends(get_budget_repository)],
) -> BudgetResponseDTO:
    """Cria um novo orçamento."""
    use_case = CreateBudgetUseCase(budget_repository)

    try:
        return await use_case.execute(current_user.id, dto)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/", response_model=list[BudgetResponseDTO])
async def list_budgets(
    current_user: CurrentUser,
    budget_repository: Annotated[BudgetRepositoryImpl, Depends(get_budget_repository)],
    transaction_repository: Annotated[TransactionRepositoryImpl, Depends(get_transaction_repository)],
    month: int = Query(default_factory=lambda: datetime.utcnow().month, ge=1, le=12),
    year: int = Query(default_factory=lambda: datetime.utcnow().year, ge=2000),
) -> list[BudgetResponseDTO]:
    """Lista os orçamentos do usuário para um período."""
    use_case = GetBudgetsUseCase(budget_repository, transaction_repository)
    return await use_case.execute(current_user.id, month, year)


@router.patch("/{budget_id}", response_model=BudgetResponseDTO)
async def update_budget(
    budget_id: UUID,
    dto: BudgetUpdateDTO,
    current_user: CurrentUser,
    budget_repository: Annotated[BudgetRepositoryImpl, Depends(get_budget_repository)],
) -> BudgetResponseDTO:
    """Atualiza um orçamento."""
    use_case = UpdateBudgetUseCase(budget_repository)
    result = await use_case.execute(budget_id, current_user.id, dto)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orçamento não encontrado",
        )

    return result


@router.delete("/{budget_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_budget(
    budget_id: UUID,
    current_user: CurrentUser,
    budget_repository: Annotated[BudgetRepositoryImpl, Depends(get_budget_repository)],
) -> None:
    """Remove um orçamento."""
    use_case = DeleteBudgetUseCase(budget_repository)
    success = await use_case.execute(budget_id, current_user.id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orçamento não encontrado",
        )
