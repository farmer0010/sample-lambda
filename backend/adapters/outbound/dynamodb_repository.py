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
            "content_lower": memo.content.lower(),
            "created_at": memo.created_at,
            "GSI1PK": f"USER#{memo.user_id}",
            "GSI1SK": memo.created_at,
        }
        self.table.put_item(Item=item)

    def get_all(
        self, user_id: str, category: str | None, limit: int, search: str | None
    ) -> list[Memo]:
        query_params: dict[str, Any] = {
            "IndexName": "GSI1",
            "KeyConditionExpression": Key("GSI1PK").eq(f"USER#{user_id}"),
            "ScanIndexForward": False,
        }

        filter_expression = []
        expression_attribute_values = {}

        if category:
            filter_expression.append("category = :category")
            expression_attribute_values[":category"] = category
        if search:
            filter_expression.append("contains(content_lower, :search)")
            expression_attribute_values[":search"] = search.lower()
        if filter_expression:
            query_params["FilterExpression"] = " AND ".join(filter_expression)
            query_params["ExpressionAttributeValues"] = expression_attribute_values

        if not category and not search:
            query_params["Limit"] = limit

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
