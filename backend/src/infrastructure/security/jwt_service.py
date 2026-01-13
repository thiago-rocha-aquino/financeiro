from datetime import datetime, timedelta
from typing import Any, Optional
from uuid import UUID

from jose import JWTError, jwt

from src.infrastructure.config import Settings


class JWTService:
    """Serviço para criação e validação de tokens JWT."""

    def __init__(self, settings: Settings) -> None:
        self._secret_key = settings.jwt_secret_key
        self._algorithm = settings.jwt_algorithm
        self._expire_minutes = settings.jwt_expire_minutes

    def create_access_token(self, data: dict[str, Any]) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self._expire_minutes)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self._secret_key, algorithm=self._algorithm)

    def decode_token(self, token: str) -> Optional[dict[str, Any]]:
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
            return payload
        except JWTError:
            return None

    def get_user_id_from_token(self, token: str) -> Optional[UUID]:
        payload = self.decode_token(token)
        if not payload:
            return None

        user_id = payload.get("sub")
        if not user_id:
            return None

        try:
            return UUID(user_id)
        except ValueError:
            return None
