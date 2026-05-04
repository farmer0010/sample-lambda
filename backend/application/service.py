from backend.domain.memo import Memo
from backend.application.ports import MemoRepository

class MemoService:
    def __init__(self, repo: MemoRepository):
        self.repo = repo

    def create_memo(self, content: str, category: str = "cli") -> Memo:
        """메모 생성 유스케이스"""
        new_memo = Memo(content=content, category=category)
        self.repo.save(new_memo)
        return new_memo