from datetime import datetime
from typing import Annotated, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.application.dtos import (
    TransactionCreateDTO,
    TransactionResponseDTO,
    TransactionUpdateDTO,
)
from src.application.use_cases import (
    CreateTransactionUseCase,
    DeleteTransactionUseCase,
    GetTransactionsUseCase,
    GetTransactionSummaryUseCase,
)
from src.application.use_cases.transaction_use_cases import TransactionSummaryDTO
from src.domain.entities import TransactionType
from src.infrastructure.database.repositories import TransactionRepositoryImpl
from src.presentation.api.dependencies import CurrentUser, get_transaction_repository

router = APIRouter(prefix="/transactions", tags=["Transações"])


@router.post("/", response_model=TransactionResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    dto: TransactionCreateDTO,
    current_user: CurrentUser,
    transaction_repository: Annotated[TransactionRepositoryImpl, Depends(get_transaction_repository)],
) -> TransactionResponseDTO:
    """Cria uma nova transação."""
    use_case = CreateTransactionUseCase(transaction_repository)
    return await use_case.execute(current_user.id, dto)


@router.get("/", response_model=list[TransactionResponseDTO])
async def list_transactions(
    current_user: CurrentUser,
    transaction_repository: Annotated[TransactionRepositoryImpl, Depends(get_transaction_repository)],
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    type: Optional[TransactionType] = Query(None),
    category_id: Optional[UUID] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
) -> list[TransactionResponseDTO]:
    """Lista as transações do usuário com filtros opcionais."""
    use_case = GetTransactionsUseCase(transaction_repository)
    return await use_case.execute(
        user_id=current_user.id,
        start_date=start_date,
        end_date=end_date,
        type=type,
        category_id=category_id,
        limit=limit,
        offset=offset,
    )


@router.get("/summary", response_model=TransactionSummaryDTO)
async def get_summary(
    current_user: CurrentUser,
    transaction_repository: Annotated[TransactionRepositoryImpl, Depends(get_transaction_repository)],
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
) -> TransactionSummaryDTO:
    """Retorna o resumo das transações do usuário."""
    use_case = GetTransactionSummaryUseCase(transaction_repository)
    return await use_case.execute(
        user_id=current_user.id,
        start_date=start_date,
        end_date=end_date,
    )


@router.get("/monthly")
async def get_monthly_summary(
    current_user: CurrentUser,
    transaction_repository: Annotated[TransactionRepositoryImpl, Depends(get_transaction_repository)],
    year: int = Query(default_factory=lambda: datetime.now().year),
) -> list[dict]:
    """Retorna o resumo mensal das transações do usuário."""
    from calendar import monthrange

    monthly_data = []
    month_names = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]

    for month in range(1, 13):
        start_date = datetime(year, month, 1)
        _, last_day = monthrange(year, month)
        end_date = datetime(year, month, last_day, 23, 59, 59)

        income = await transaction_repository.get_total_by_type(
            user_id=current_user.id,
            type=TransactionType.INCOME,
            start_date=start_date,
            end_date=end_date,
        )

        expense = await transaction_repository.get_total_by_type(
            user_id=current_user.id,
            type=TransactionType.EXPENSE,
            start_date=start_date,
            end_date=end_date,
        )

        monthly_data.append({
            "name": month_names[month - 1],
            "receitas": float(income),
            "despesas": float(expense),
        })

    return monthly_data


@router.patch("/{transaction_id}", response_model=TransactionResponseDTO)
async def update_transaction(
    transaction_id: UUID,
    dto: TransactionUpdateDTO,
    current_user: CurrentUser,
    transaction_repository: Annotated[TransactionRepositoryImpl, Depends(get_transaction_repository)],
) -> TransactionResponseDTO:
    """Atualiza uma transação."""
    from src.application.use_cases import UpdateTransactionUseCase

    use_case = UpdateTransactionUseCase(transaction_repository)
    result = await use_case.execute(transaction_id, current_user.id, dto)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transação não encontrada",
        )

    return result


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    transaction_id: UUID,
    current_user: CurrentUser,
    transaction_repository: Annotated[TransactionRepositoryImpl, Depends(get_transaction_repository)],
) -> None:
    """Remove uma transação."""
    use_case = DeleteTransactionUseCase(transaction_repository)
    success = await use_case.execute(transaction_id, current_user.id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transação não encontrada",
        )
