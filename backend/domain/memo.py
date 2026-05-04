from dataclasses import dataclass, field
import uuid
from datetime import datetime

@dataclass
class Memo:
    """메모 도메인 모델"""
    content: str
    category: str = "cli"
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def __post_init__(self):
        if not self.content or not self.content.strip():
            raise ValueError("메모 내용을 비어있을 수 없습니다.")
        if len(self.content) > 500:
            raise ValueError("메모는 500자 이상 넘을 수 없습니다.")