from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from src.application.dtos import UserResponseDTO, UserUpdateDTO
from src.application.use_cases import GetUserUseCase, UpdateUserUseCase
from src.infrastructure.database.repositories import UserRepositoryImpl
from src.presentation.api.dependencies import CurrentUser, get_user_repository

router = APIRouter(prefix="/users", tags=["Usuários"])


@router.get("/me", response_model=UserResponseDTO)
async def get_current_user_info(current_user: CurrentUser) -> UserResponseDTO:
    """Retorna as informações do usuário autenticado."""
    return UserResponseDTO.model_validate(current_user)


@router.patch("/me", response_model=UserResponseDTO)
async def update_current_user(
    dto: UserUpdateDTO,
    current_user: CurrentUser,
    user_repository: Annotated[UserRepositoryImpl, Depends(get_user_repository)],
) -> UserResponseDTO:
    """Atualiza as informações do usuário autenticado."""
    use_case = UpdateUserUseCase(user_repository)
    result = await use_case.execute(current_user.id, dto)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado",
        )

    return result
