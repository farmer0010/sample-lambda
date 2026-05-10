from abc import ABC, abstractmethod
from typing import List

from backend.domain.memo import Memo

class MemoRepository(ABC):
    """
    """
    @abstractmethod
    def save(self, memo: Memo):
        """메모를 저장합니다."""
        pass

    @abstractmethod
    def get_all(self) -> List[Memo]:
        """모든 메모를 가져옵니다"""
        pass