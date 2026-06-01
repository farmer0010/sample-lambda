import boto3
from boto3.dynamodb.conditions import Key

from backend.application.ports import MemoRepository
from backend.domain.memo import Memo


class DynamoDBRepository(MemoRepository):
    def __init__(self, table_name: str, table=None):
        if table is not None:
            self.table = table
        else:
            self.dynamodb = boto3.resource("dynamodb", region_name="ap-northeast-2")
            self.table = self.dynamodb.Table(table_name)

    def save(self, memo: Memo) -> None:
        item = {
            "PK": f"MEMO#{memo.id}",
            "SK": "METADATA",
            "user_id": memo.user_id,
            "category": memo.category,
            "content": memo.content,
            "created_at": memo.created_at,
            "GSI1PK": f"USER#{memo.user_id}",
            "GSI1SK": memo.created_at,
            "GSI2PK": f"USER#{memo.user_id}#CATEGORY#{memo.category}",
            "GSI2SK": memo.created_at,
        }
        self.table.put_item(Item=item)

    def get_all(
        self, user_id: str, category: str | None, limit: int, search: str | None
    ) -> list[Memo]:
        if category:
            response = self.table.query(
                IndexName="GSI2",
                KeyConditionExpression=Key("GSI2PK").eq(
                    f"USER#{user_id}#CATEGORY#{category}"
                ),
                ScanIndexForward=False,
            )
        else:
            response = self.table.query(
                IndexName="GSI1",
                KeyConditionExpression=Key("GSI1PK").eq(f"USER#{user_id}"),
                ScanIndexForward=False,
            )
        items = response.get("Items", [])

        memos = []

        for item in items:
            item_category = item.get("category", "basic")

            if search and search.lower() not in item.get("content", "").lower():
                continue

            _, memo_id = item.get("PK").split("#")

            memos.append(
                Memo(
                    id=memo_id,
                    user_id=item["user_id"],
                    content=item["content"],
                    category=item_category,
                    created_at=item.get("created_at", ""),
                )
            )

        return memos[:limit]
