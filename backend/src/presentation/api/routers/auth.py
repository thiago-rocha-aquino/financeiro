from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.application.dtos import LoginDTO, TokenDTO, UserCreateDTO, UserResponseDTO
from src.application.use_cases import CreateUserUseCase, LoginUseCase
from src.infrastructure.database.repositories import UserRepositoryImpl
from src.infrastructure.security import JWTService, PasswordServiceImpl
from src.presentation.api.dependencies import (
    get_jwt_service,
    get_password_service,
    get_user_repository,
)

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/register", response_model=UserResponseDTO, status_code=status.HTTP_201_CREATED)
async def register(
    dto: UserCreateDTO,
    user_repository: Annotated[UserRepositoryImpl, Depends(get_user_repository)],
    password_service: Annotated[PasswordServiceImpl, Depends(get_password_service)],
) -> UserResponseDTO:
    """Registra um novo usuário."""
    use_case = CreateUserUseCase(user_repository, password_service)

    try:
        return await use_case.execute(dto)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/login", response_model=TokenDTO)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_repository: Annotated[UserRepositoryImpl, Depends(get_user_repository)],
    password_service: Annotated[PasswordServiceImpl, Depends(get_password_service)],
    jwt_service: Annotated[JWTService, Depends(get_jwt_service)],
) -> TokenDTO:
    """Autentica um usuário e retorna o token de acesso."""
    use_case = LoginUseCase(user_repository, password_service, jwt_service)

    dto = LoginDTO(email=form_data.username, password=form_data.password)
    result = await use_case.execute(dto)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return result
