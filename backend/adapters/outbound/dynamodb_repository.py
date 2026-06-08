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
            self.dynamodb = boto3.resource("dynamodb", region_name="ap-northeast-2")
            self.table = self.dynamodb.Table(table_name)

    def save(self, memo: Memo) -> None:
        item = {
            "PK": f"USER#{memo.user_id}",
            "SK": f"MEMO#{memo.id}",
            "user_id": memo.user_id,
            "category": memo.category,
            "content": memo.content,
            "created_at": memo.created_at,
            "GSI1PK": f"MEMO#{memo.id}",
            "GSI1SK": f"USER#{memo.user_id}",
            "GSI2PK": f"USER#{memo.user_id}#CATEGORY#{memo.category}",
            "GSI2SK": f"MEMO#{memo.id}",
        }
        self.table.put_item(Item=item)

    def get_all(self, user_id: str, category: str | None, limit: int) -> list[Memo]:
        query_params: dict[str, Any] = {
            "ScanIndexForward": False,
            "Limit": limit,
        }

        if category:
            query_params["IndexName"] = "GSI2"
            query_params["KeyConditionExpression"] = Key("GSI2PK").eq(
                f"USER#{user_id}#CATEGORY#{category}"
            )
        else:
            query_params["KeyConditionExpression"] = Key("PK").eq(f"USER#{user_id}")

        response = self.table.query(**query_params)
        items = response.get("Items", [])

        memos = []

        for item in items:
            item_category = item.get("category", "basic")

            _, memo_id = item.get("SK", "").split("#")

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

    def get_by_id(self, memo_id: str) -> Memo | None:
        response = self.table.query(
            IndexName="GSI1",
            KeyConditionExpression=Key("GSI1PK").eq(f"MEMO#{memo_id}"),
        )
        items = response.get("Items", [])
        if not items:
            return None

        item = items[0]
        item_category = item.get("category", "basic")
        _, extracted_id = item.get("SK", "").split("#")
        return Memo(
            id=extracted_id,
            user_id=item["user_id"],
            content=item["content"],
            category=item_category,
            created_at=item.get("created_at", ""),
        )
