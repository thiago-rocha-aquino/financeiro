from abc import ABC, abstractmethod


class PasswordService(ABC):
    """Interface abstrata para o serviço de senhas."""

    @abstractmethod
    def hash_password(self, password: str) -> str:
        """Gera o hash de uma senha."""
        pass

    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verifica se uma senha corresponde ao hash."""
        pass
