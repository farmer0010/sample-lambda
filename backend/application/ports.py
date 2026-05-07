from abc import ABC, abstractmethod

from backend.domain.memo import Memo


class MemoRepository(ABC):
    """
    // 인터페이스 (아웃고잉 포트)
    이 규칙을 상속 받는 DB 어뎁터는 무조건 아래 함수들을 구현해야함
    """

    @abstractmethod
    def save(self, memo: Memo):
        """메모를 저장합니다."""
        pass

    @abstractmethod
    def get_all(
        self, category: str | None = None, limit: int = 5, search: str | None = None
    ) -> list[Memo]:
        """조건에 맞는 메모들을 가져옵니다."""
        pass
