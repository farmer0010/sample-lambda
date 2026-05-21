import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone


class MemoDomainError(Exception):
    pass


@dataclass
class Memo:
    content: str
    category: str = "basic"
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def __post_init__(self):
        if not self.content or not self.content.strip():
            raise MemoDomainError("메모 내용을 비어있을 수 없습니다.")
        if len(self.content) > 1500:
            raise MemoDomainError("메모는 1500자를 초과할 수 없습니다.")
        if self.category and len(self.category) > 30:
            raise MemoDomainError("카테고리 이름은 30자를 초과할 수 없습니다.")
