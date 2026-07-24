from abc import ABC, abstractmethod


class TokenStoragePort(ABC):
    @abstractmethod
    def get_token(self) -> str | None:
        pass

    @abstractmethod
    def save_token(self, token: str) -> None:
        pass

    @abstractmethod
    def delete_token(self) -> bool:
        pass


class MemoRepositoryPort(ABC):
    @abstractmethod
    def save(self, token: str, content: str, category: str | None = None) -> dict:
        pass

    @abstractmethod
    def get_all(self, token: str, category: str | None = None, limit: int = 5) -> list:
        pass

    @abstractmethod
    def update(self, memo_id: str, token: str, content: str) -> dict:
        pass

    @abstractmethod
    def delete(self, memo_id: str, token: str) -> dict:
        pass


class AuthRepositoryPort(ABC):
    @abstractmethod
    def request_device_code(self) -> dict:
        pass

    @abstractmethod
    def poll_for_token(self, device_code: str, interval: int = 5) -> dict:
        pass
