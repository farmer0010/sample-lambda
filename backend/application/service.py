from typing import List

from backend.application.ports import MemoRepository, MemoUseCase
from backend.domain.memo import Memo


class MemoService(MemoUseCase):
    def __init__(self, repo: MemoRepository):
        self.repo = repo

    def create_memo(
        self, user_id: str, content: str, category: str | None = None
    ) -> Memo:
        if category is not None:
            new_memo = Memo(user_id=user_id, content=content, category=category)
        else:
            new_memo = Memo(user_id=user_id, content=content)
        self.repo.save(new_memo)
        return new_memo

    def get_all_memos(
        self, user_id: str, category: str | None, limit: int
    ) -> List[Memo]:
        return self.repo.get_all(user_id=user_id, category=category, limit=limit)

    def get_memo_by_id(self, memo_id: str) -> Memo | None:
        return self.repo.get_by_id(memo_id)
