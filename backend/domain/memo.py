import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Memo:
    """메모 도메인 모델"""

    content: str
    category: str = "basic"
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def __post_init__(self):
        if not self.content or not self.content.strip():
            raise ValueError("메모 내용을 비어있을 수 없습니다.")
        if len(self.content) > 1500:
            raise ValueError("메모는 1500자 이상 넘을 수 없습니다.")
        if self.category and len(self.category) > 30:
            raise ValueError("카테고리 이름은 30자 이상을 초과할 수 없습니다")
