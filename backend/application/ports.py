from abc import ABC, abstractmethod
from typing import List

from backend.domain.memo import Memo


class MemoUseCase(ABC):
    @abstractmethod
    def create_memo(self, content: str, category: str | None = None) -> Memo:
        pass

    @abstractmethod
    def get_all_memos(
        self, category: str | None, limit: int, search: str | None
    ) -> List[Memo]:
        pass


class MemoRepository(ABC):
    @abstractmethod
    def save(self, memo: Memo):
        pass

    @abstractmethod
    def get_all(
        self, category: str | None, limit: int, search: str | None
    ) -> List[Memo]:
        pass
