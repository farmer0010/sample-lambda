from abc import ABC, abstractmethod


class MemoUseCase(ABC):
    @abstractmethod
    def save_memo(self, content: str, category: str | None = None) -> dict:
        pass

    @abstractmethod
    def get_memos(self, category: str | None = None, limit: int = 5) -> list:
        pass

    @abstractmethod
    def update_memo(self, memo_id: str, content: str) -> dict:
        pass

    @abstractmethod
    def delete_memo(self, memo_id: str) -> dict:
        pass


class AuthUseCase(ABC):
    @abstractmethod
    def request_login(self) -> dict:
        pass

    @abstractmethod
    def complete_login(self, device_code: str, interval: int) -> bool:
        pass

    @abstractmethod
    def logout(self) -> bool:
        pass
