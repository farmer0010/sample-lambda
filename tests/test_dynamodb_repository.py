from unittest.mock import MagicMock

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
    )


def setup_mock_table():
    mock_table = MagicMock()
    mock_table.query.return_value = {
        "Items": [
            {
                "PK": "MEMO#4",
                "SK": "METADATA",
                "user_id": "testUser",
                "content": "파이썬 메모",
                "category": "python",
                "created_at": "2025-05-22T12:00:00",
            },
            {
                "PK": "MEMO#3",
                "SK": "METADATA",
                "user_id": "testUser",
                "content": "자바 메모입니다",
                "category": "java",
                "created_at": "2025-05-21T11:00:00",
            },
            {
                "PK": "MEMO#2",
                "SK": "METADATA",
                "user_id": "testUser",
                "content": "두 번째 기본 메모",
                "category": "basic",
                "created_at": "2025-05-21T10:10:00",
            },
            {
                "PK": "MEMO#1",
                "SK": "METADATA",
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

    memos = repo.get_all(user_id="testUser", category=None, limit=2, search=None)
    assert len(memos) == 2
    assert memos[0].id == "4"


def test_get_memos_filter_by_category():
    mock_table = setup_mock_table()

    mock_table.query.return_value = {
        "Items": [
            {
                "PK": "MEMO#3",
                "SK": "METADATA",
                "user_id": "user123",
                "content": "자바 메모입니다",
                "category": "java",
                "created_at": "2025-05-21T11:00:00",
            }
        ]
    }
    repo = DynamoDBRepository(table_name="test-table", table=mock_table)

    java_memos = repo.get_all(user_id="testUser", category="java", limit=5, search=None)
    assert len(java_memos) == 1
    assert java_memos[0].id == "3"


def test_get_memos_filter_search_keword():
    mock_table = setup_mock_table()
    repo = DynamoDBRepository(table_name="test-table", table=mock_table)

    search_memos = repo.get_all(
        user_id="testUser", category=None, limit=5, search="파이썬"
    )
    assert len(search_memos) == 1
    assert search_memos[0].id == "4"


def test_get_memos_empty_search():
    mock_table = setup_mock_table()
    repo = DynamoDBRepository(table_name="test-table", table=mock_table)

    empty_memos = repo.get_all(
        user_id="testUser", category=None, limit=5, search="러스트"
    )
    assert len(empty_memos) == 0
