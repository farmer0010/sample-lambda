from abc import ABC, abstractmethod
from typing import List

from backend.domain.memo import Memo


class MemoUseCase(ABC):
    @abstractmethod
    def create_memo(
        self, user_id: str, content: str, category: str | None = None
    ) -> Memo:
        pass

    @abstractmethod
    def get_all_memos(
        self, user_id: str, category: str | None, limit: int
    ) -> List[Memo]:
        pass

    @abstractmethod
    def get_memo_by_id(self, memo_id: str, user_id: str) -> Memo | None:
        pass

    @abstractmethod
    def update_memo(self, memo_id: str, user_id: str, content: str) -> Memo:
        pass

    @abstractmethod
    def delete_memo(self, memo_id: str, user_id: str) -> None:
        pass


class MemoRepository(ABC):
    @abstractmethod
    def save(self, memo: Memo) -> None:
        pass

    @abstractmethod
    def get_all(self, user_id: str, category: str | None, limit: int) -> List[Memo]:
        pass

    @abstractmethod
    def get_by_id(self, memo_id: str) -> Memo | None:
        pass
