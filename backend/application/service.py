from typing import List

from backend.application.ports import MemoRepository, MemoUseCase
from backend.domain.memo import Memo


class MemoService(MemoUseCase):
    def __init__(self, repo: MemoRepository):
        self.repo = repo

    def create_memo(self, content: str, category: str | None = None) -> Memo:
        if category is not None:
            new_memo = Memo(content=content, category=category)
        else:
            new_memo = Memo(content=content)
        self.repo.save(new_memo)
        return new_memo

    def get_all_memos(
        self, category: str | None, limit: int, search: str | None
    ) -> List[Memo]:
        return self.repo.get_all(category=category, limit=limit, search=search)
