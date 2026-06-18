from dataclasses import dataclass, field
from datetime import datetime, timezone

from ulid import ULID


class MemoDomainError(Exception):
    pass


@dataclass
class Memo:
    content: str
    user_id: str
    category: str | None = "basic"
    id: str = field(default_factory=lambda: str(ULID()))
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def __post_init__(self):
        if self.category is None or self.category.strip() == "":
            self.category = "basic"

        self._validate_content(self.content)
        if self.category and len(self.category) > 30:
            raise MemoDomainError("카테고리 이름은 30자를 초과할 수 없습니다.")
        if not self.user_id or not self.user_id.strip():
            raise MemoDomainError("유저 식별자는 비어있을 수 없습니다.")

    @staticmethod
    def _validate_content(content: str) -> None:
        if not content or not content.strip():
            raise MemoDomainError("메모 내용은 비어있을 수 없습니다.")
        if len(content) > 1500:
            raise MemoDomainError("메모는 1500자를 초과할 수 없습니다.")

    def update_content(self, new_content: str) -> None:
        self._validate_content(new_content)
        self.content = new_content
