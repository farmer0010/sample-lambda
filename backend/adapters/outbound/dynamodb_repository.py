import boto3

from backend.application.ports import MemoRepository
from backend.domain.memo import Memo


class DynamoDBRepository(MemoRepository):
    def __init__(self, table_name: str):
        self.dynamodb = boto3.resource("dynamodb", region_name="ap-northeast-2")
        self.table = self.dynamodb.Table(table_name)

    def save(self, memo: Memo) -> None:
        item = {
            "PK": f"MEMO#{memo.id}",
            "SK": memo.created_at,
            "category": memo.category,
            "content": memo.content,
            "created_at": memo.created_at,
        }
        self.table.put_item(Item=item)

    def get_all(
        self, category: str | None, limit: int, search: str | None
    ) -> list[Memo]:
        response = self.table.scan()
        items = response.get("Items", [])

        memos = []

        for item in items:
            if category and item.get("category") != category:
                continue

            if search and search.lower() not in item.get("content", "").lower():
                continue

            memos.append(
                Memo(
                    id=item["PK"].replace("MEMO#", ""),
                    content=item["content"],
                    category=item.get("category", "basic"),
                    created_at=item.get("created_at", ""),
                )
            )

        memos.sort(key=lambda x: x.created_at, reverse=True)

        return memos[:limit]
