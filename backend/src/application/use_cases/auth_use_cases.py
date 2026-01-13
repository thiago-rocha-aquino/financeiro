from typing import Optional

from src.application.dtos import LoginDTO, TokenDTO
from src.domain.repositories import UserRepository
from src.domain.services import PasswordService
from src.infrastructure.security.jwt_service import JWTService


class LoginUseCase:
    """Caso de uso para autenticação."""

    def __init__(
        self,
        user_repository: UserRepository,
        password_service: PasswordService,
        jwt_service: JWTService,
    ):
        self._user_repository = user_repository
        self._password_service = password_service
        self._jwt_service = jwt_service

    async def execute(self, dto: LoginDTO) -> Optional[TokenDTO]:
        user = await self._user_repository.get_by_email(dto.email)

        if not user:
            return None

        if not self._password_service.verify_password(dto.password, user.hashed_password):
            return None

        if not user.is_active:
            return None

        access_token = self._jwt_service.create_access_token(
            data={"sub": str(user.id), "email": user.email}
        )

        return TokenDTO(access_token=access_token)
