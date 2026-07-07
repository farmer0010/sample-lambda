from datetime import datetime
from typing import Any

import boto3
from boto3.dynamodb.conditions import Key

from backend.application.ports import MemoRepository
from backend.domain.memo import Memo


class DynamoDBRepository(MemoRepository):
    def __init__(self, table_name: str, table=None):
        if table is not None:
            self.table = table
        else:
            self.dynamodb = boto3.resource(
                "dynamodb",
                region_name="ap-northeast-2",
            )
            self.table = self.dynamodb.Table(table_name)

    def _to_domain(self, item: dict[str, Any]) -> Memo:
        _, memo_id = item.get("SK", "").split("#")

        created_at_str = item["created_at"]
        created_at = datetime.fromisoformat(created_at_str)

        updated_at_str = item.get("updated_at")
        updated_at = datetime.fromisoformat(updated_at_str) if updated_at_str else None

        return Memo(
            id=memo_id,
            user_id=item["user_id"],
            content=item["content"],
            category=item.get("category"),
            created_at=created_at,
            updated_at=updated_at,
        )

    def save(self, memo: Memo) -> None:
        if memo.is_deleted:
            self.table.delete_item(
                Key={"PK": f"USER#{memo.user_id}", "SK": f"MEMO#{memo.id}"},
            )
            return

        item = {
            "PK": f"USER#{memo.user_id}",
            "SK": f"MEMO#{memo.id}",
            "user_id": memo.user_id,
            "category": memo.category,
            "content": memo.content,
            "created_at": memo.created_at.isoformat(),
            "updated_at": (
                memo.updated_at.isoformat() if memo.updated_at is not None else None
            ),
            "LSI1SK": f"C#{memo.category}#M#{memo.id}",
        }
        self.table.put_item(Item=item)

    def get_all(
        self,
        user_id: str,
        category: str | None,
        limit: int,
    ) -> list[Memo]:
        query_params: dict[str, Any] = {
            "ScanIndexForward": False,
            "Limit": limit,
        }

        if category:
            query_params["IndexName"] = "CategoryIndex"
            query_params["KeyConditionExpression"] = Key("PK").eq(
                f"USER#{user_id}"
            ) & Key("LSI1SK").begins_with(f"C#{category}#")
        else:
            query_params["KeyConditionExpression"] = Key("PK").eq(f"USER#{user_id}")

        response = self.table.query(**query_params)
        items = response.get("Items", [])

        return [self._to_domain(item) for item in items][:limit]

    def get_by_id(self, memo_id: str) -> Memo | None:
        response = self.table.query(
            IndexName="MemoLookupIndex",
            KeyConditionExpression=Key("SK").eq(f"MEMO#{memo_id}"),
        )
        items = response.get("Items", [])
        if not items:
            return None

        return self._to_domain(items[0])
