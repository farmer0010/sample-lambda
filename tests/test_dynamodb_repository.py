from unittest.mock import MagicMock

from boto3.dynamodb.conditions import Key

from backend.adapters.outbound.dynamodb_repository import DynamoDBRepository
from backend.domain.memo import Memo


def test_save_memo():
    mock_table = MagicMock()

    repo = DynamoDBRepository(table_name="test-table", table=mock_table)
    memo = Memo(
        content="내장 Mock으로 테스트하는 메모!", user_id="testUser", category="test"
    )

    repo.save(memo)

    mock_table.put_item.assert_called_once_with(
        Item={
            "PK": f"USER#{memo.user_id}",
            "SK": f"MEMO#{memo.id}",
            "user_id": memo.user_id,
            "category": memo.category,
            "content": memo.content,
            "created_at": memo.created_at,
            "LSI1SK": f"C#{memo.category}#M#{memo.id}",
        }
    )


def setup_mock_table():
    mock_table = MagicMock()
    mock_table.query.return_value = {
        "Items": [
            {
                "PK": "USER#testUser",
                "SK": "MEMO#4",
                "user_id": "testUser",
                "content": "파이썬 메모",
                "category": "python",
                "created_at": "2025-05-22T12:00:00",
            },
            {
                "PK": "USER#testUser",
                "SK": "MEMO#3",
                "user_id": "testUser",
                "content": "자바 메모입니다",
                "category": "java",
                "created_at": "2025-05-21T11:00:00",
            },
            {
                "PK": "USER#testUser",
                "SK": "MEMO#2",
                "user_id": "testUser",
                "content": "두 번째 기본 메모",
                "category": "basic",
                "created_at": "2025-05-21T10:10:00",
            },
            {
                "PK": "USER#testUser",
                "SK": "MEMO#1",
                "user_id": "testUser",
                "content": "첫 번째 기본 메모",
                "category": "basic",
                "created_at": "2025-05-21T10:00:00",
            },
        ]
    }
    return mock_table


def test_get_memos_limit_and_sort():
    mock_table = setup_mock_table()
    repo = DynamoDBRepository(table_name="test-table", table=mock_table)

    memos = repo.get_all(user_id="testUser", category=None, limit=2)
    assert len(memos) == 2
    assert memos[0].id == "4"

    mock_table.query.assert_called_once_with(
        KeyConditionExpression=Key("PK").eq("USER#testUser"),
        ScanIndexForward=False,
        Limit=2,
    )


def test_get_memos_filter_by_category():
    mock_table = MagicMock()
    mock_table.query.return_value = {
        "Items": [
            {
                "PK": "USER#testUser",
                "SK": "MEMO#3",
                "user_id": "testUser",
                "content": "자바 메모입니다",
                "category": "java",
                "created_at": "2025-05-21T11:00:00",
            }
        ]
    }
    repo = DynamoDBRepository(table_name="test-table", table=mock_table)

    java_memos = repo.get_all(user_id="testUser", category="java", limit=5)
    assert len(java_memos) == 1
    assert java_memos[0].id == "3"

    mock_table.query.assert_called_once_with(
        IndexName="CategoryIndex",
        KeyConditionExpression=Key("PK").eq("USER#testUser")
        & Key("LSI1SK").begins_with("C#java#"),
        ScanIndexForward=False,
        Limit=5,
    )


def test_get_memo_by_id():
    mock_table = MagicMock()
    mock_table.query.return_value = {
        "Items": [
            {
                "PK": "USER#testUser",
                "SK": "MEMO#123",
                "user_id": "testUser",
                "content": "단건 조회 테스트 메모",
                "category": "basic",
                "created_at": "2025-05-21T10:00:00",
            }
        ]
    }
    repo = DynamoDBRepository(table_name="test-table", table=mock_table)

    memo = repo.get_by_id("123")
    assert memo is not None
    assert memo.id == "123"
    assert memo.content == "단건 조회 테스트 메모"

    mock_table.query.assert_called_once_with(
        IndexName="MemoLookupIndex",
        KeyConditionExpression=Key("SK").eq("MEMO#123"),
    )
