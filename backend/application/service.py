from backend.domain.memo import Memo
from backend.application.ports import MemoRepository

class MemoService:
    def __init__(self, repo: MemoRepository):
        self.repo = repo

    def create_memo(self, content: str, category: str | None = None) -> Memo:
        if category is not None:
            new_memo = Memo(content=content, category=category)
        else:
            new_memo = Memo(content=content)
        self.repo.save(new_memo)
        return new_memo