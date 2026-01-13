from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities import User
from src.infrastructure.config import Settings, get_settings
from src.infrastructure.database import get_db
from src.infrastructure.database.repositories import (
    BudgetRepositoryImpl,
    CategoryRepositoryImpl,
    TransactionRepositoryImpl,
    UserRepositoryImpl,
)
from src.infrastructure.security import JWTService, PasswordServiceImpl

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_password_service() -> PasswordServiceImpl:
    return PasswordServiceImpl()


def get_jwt_service(
    settings: Annotated[Settings, Depends(get_settings)]
) -> JWTService:
    return JWTService(settings)


def get_user_repository(
    session: Annotated[AsyncSession, Depends(get_db)]
) -> UserRepositoryImpl:
    return UserRepositoryImpl(session)


def get_category_repository(
    session: Annotated[AsyncSession, Depends(get_db)]
) -> CategoryRepositoryImpl:
    return CategoryRepositoryImpl(session)


def get_transaction_repository(
    session: Annotated[AsyncSession, Depends(get_db)]
) -> TransactionRepositoryImpl:
    return TransactionRepositoryImpl(session)


def get_budget_repository(
    session: Annotated[AsyncSession, Depends(get_db)]
) -> BudgetRepositoryImpl:
    return BudgetRepositoryImpl(session)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_service: Annotated[JWTService, Depends(get_jwt_service)],
    user_repository: Annotated[UserRepositoryImpl, Depends(get_user_repository)],
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user_id = jwt_service.get_user_id_from_token(token)
    if not user_id:
        raise credentials_exception

    user = await user_repository.get_by_id(user_id)
    if not user:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo",
        )

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
