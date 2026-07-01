from typing import List

from backend.application.exceptions import MemoAccessDeniedError
from backend.application.ports import MemoRepository, MemoUseCase
from backend.domain.memo import Memo


class MemoService(MemoUseCase):
    def __init__(self, repo: MemoRepository):
        self.repo = repo

    def create_memo(
        self, user_id: str, content: str, category: str | None = None
    ) -> Memo:
        new_memo = Memo(user_id=user_id, content=content, category=category)
        self.repo.save(new_memo)
        return new_memo

    def get_all_memos(
        self, user_id: str, category: str | None, limit: int
    ) -> List[Memo]:
        return self.repo.get_all(user_id=user_id, category=category, limit=limit)

    def get_memo_by_id(self, memo_id: str, user_id: str) -> Memo | None:
        memo = self.repo.get_by_id(memo_id)
        if not memo:
            return None
        if memo.user_id != user_id:
            return None
        return memo

    def update_memo(self, memo_id: str, user_id: str, content: str) -> Memo:
        memo = self.repo.get_by_id(memo_id)
        if not memo or memo.user_id != user_id:
            raise MemoAccessDeniedError("메모를 찾을 수 없거나 수정 권한이 없습니다.")
        memo.update_content(content)
        self.repo.save(memo)
        return memo
