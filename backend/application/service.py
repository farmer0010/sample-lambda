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

    def get_all_memos(self, category: str = None, limit: int = 5, search: str = None) -> list[Memo]:
        """조건에 맞는 메모 조회를 저장소에 요청합니다"""
        return self.repo.get_all(category=category, limit=limit, search=search)