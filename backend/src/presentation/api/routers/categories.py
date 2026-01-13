from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.application.dtos import CategoryCreateDTO, CategoryResponseDTO, CategoryUpdateDTO
from src.application.use_cases import (
    CreateCategoryUseCase,
    DeleteCategoryUseCase,
    GetCategoriesUseCase,
    UpdateCategoryUseCase,
)
from src.infrastructure.database.repositories import CategoryRepositoryImpl
from src.presentation.api.dependencies import CurrentUser, get_category_repository

router = APIRouter(prefix="/categories", tags=["Categorias"])


@router.post("/", response_model=CategoryResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_category(
    dto: CategoryCreateDTO,
    current_user: CurrentUser,
    category_repository: Annotated[CategoryRepositoryImpl, Depends(get_category_repository)],
) -> CategoryResponseDTO:
    """Cria uma nova categoria."""
    use_case = CreateCategoryUseCase(category_repository)
    return await use_case.execute(current_user.id, dto)


@router.get("/", response_model=list[CategoryResponseDTO])
async def list_categories(
    current_user: CurrentUser,
    category_repository: Annotated[CategoryRepositoryImpl, Depends(get_category_repository)],
) -> list[CategoryResponseDTO]:
    """Lista todas as categorias do usuário."""
    use_case = GetCategoriesUseCase(category_repository)
    return await use_case.execute(current_user.id)


@router.patch("/{category_id}", response_model=CategoryResponseDTO)
async def update_category(
    category_id: UUID,
    dto: CategoryUpdateDTO,
    current_user: CurrentUser,
    category_repository: Annotated[CategoryRepositoryImpl, Depends(get_category_repository)],
) -> CategoryResponseDTO:
    """Atualiza uma categoria."""
    use_case = UpdateCategoryUseCase(category_repository)
    result = await use_case.execute(category_id, current_user.id, dto)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoria não encontrada",
        )

    return result


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: UUID,
    current_user: CurrentUser,
    category_repository: Annotated[CategoryRepositoryImpl, Depends(get_category_repository)],
) -> None:
    """Remove uma categoria."""
    use_case = DeleteCategoryUseCase(category_repository)
    success = await use_case.execute(category_id, current_user.id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoria não encontrada",
        )
