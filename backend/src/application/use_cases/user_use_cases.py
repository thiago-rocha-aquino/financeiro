from typing import Optional
from uuid import UUID

from src.application.dtos import UserCreateDTO, UserResponseDTO, UserUpdateDTO
from src.domain.entities import User
from src.domain.repositories import UserRepository
from src.domain.services import PasswordService


class CreateUserUseCase:
    """Caso de uso para criação de usuário."""

    def __init__(
        self, user_repository: UserRepository, password_service: PasswordService
    ):
        self._user_repository = user_repository
        self._password_service = password_service

    async def execute(self, dto: UserCreateDTO) -> UserResponseDTO:
        existing_user = await self._user_repository.get_by_email(dto.email)
        if existing_user:
            raise ValueError("Email já cadastrado")

        hashed_password = self._password_service.hash_password(dto.password)

        user = User(
            email=dto.email,
            name=dto.name,
            hashed_password=hashed_password,
        )

        created_user = await self._user_repository.create(user)
        return UserResponseDTO.model_validate(created_user)


class GetUserUseCase:
    """Caso de uso para buscar usuário."""

    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    async def execute(self, user_id: UUID) -> Optional[UserResponseDTO]:
        user = await self._user_repository.get_by_id(user_id)
        if not user:
            return None
        return UserResponseDTO.model_validate(user)


class UpdateUserUseCase:
    """Caso de uso para atualizar usuário."""

    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    async def execute(self, user_id: UUID, dto: UserUpdateDTO) -> Optional[UserResponseDTO]:
        user = await self._user_repository.get_by_id(user_id)
        if not user:
            return None

        if dto.name:
            user.update_name(dto.name)

        updated_user = await self._user_repository.update(user)
        return UserResponseDTO.model_validate(updated_user)
