from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

from backend.adapters.outbound.dynamodb_repository import DynamoDBRepository
from backend.domain.memo import Memo


@patch("backend.adapters.outbound.dynamodb_repository.boto3.resource")
def test_save_memo(mock_boto_resource):
    mock_dynamodb = MagicMock()
    mock_table = MagicMock()

    mock_dynamodb.Table.return_value = mock_table
    mock_boto_resource.return_value = mock_dynamodb

    repo = DynamoDBRepository(table_name="test-table")
    memo = Memo(content="내장 Mock으로 테스트하는 메모!", category="test")

    repo.save(memo)

    mock_table.put_item.assert_called_once_with(
        Item={
            "PK": f"MEMO#{memo.id}",
            "SK": memo.created_at,
            "category": memo.category,
            "content": memo.content,
            "created_at": memo.created_at,
        }
    )


@patch("backend.adapters.outbound.dynamodb_repository.boto3.resource")
def test_save_memo_table_not_exist(mock_boto_resource):
    mock_dynamodb = MagicMock()
    mock_table = MagicMock()

    mock_dynamodb.Table.return_value = mock_table
    mock_boto_resource.return_value = mock_dynamodb

    error_response = {
        "Error": {
            "Code": "ResourceNotFoundException",
            "Message": "Requested resource not found",
        }
    }

    mock_table.put_item.side_effect = ClientError(
        error_response,
        "PutItem",
    )

    repo = DynamoDBRepository(table_name="not-exist-table")
    memo = Memo(content="존재하지 않는 테이블에 저장 시도", category="test")

    with pytest.raises(ClientError) as exc_info:
        repo.save(memo)

    assert "ResourceNotFoundException" in str(exc_info.value)


@patch("backend.adapters.outbound.dynamodb_repository.boto3.resource")
def test_get_all_memos(mock_boto3_resource):
    mock_table = MagicMock()
    mock_boto3_resource.return_value.Table.return_value = mock_table

    mock_table.scan.return_value = {
        "Items": [
            {
                "PK": "MEMO#1",
                "content": "첫 번째 기본 메모",
                "category": "basic",
                "created_at": "2025-05-21T10:00:00",
            },
            {
                "PK": "MEMO#2",
                "content": "두 번째 기본 메모",
                "category": "basic",
                "created_at": "2025-05-21T10:10:00",
            },
            {
                "PK": "MEMO#3",
                "content": "자바 메모입니다",
                "category": "java",
                "created_at": "2025-05-21T11:00:00",
            },
            {
                "PK": "MEMO#4",
                "content": "파이썬 메모",
                "category": "python",
                "created_at": "2025-05-22T12:00:00",
            },
        ]
    }
    repo = DynamoDBRepository(table_name="test-table")

    memos = repo.get_all(category=None, limit=2, search=None)
    assert len(memos) == 2
    assert memos[0].id == "4"

    java_memos = repo.get_all(category="java", limit=5, search=None)
    assert len(java_memos) == 1
    assert java_memos[0].id == "3"

    python_memos = repo.get_all(category="python", limit=5, search=None)
    assert len(python_memos) == 1
    assert python_memos[0].id == "4"

    search_memos = repo.get_all(category=None, limit=5, search="메모")
    assert len(search_memos) == 4

    empty_search_memos = repo.get_all(category=None, limit=5, search="러스트")
    assert len(empty_search_memos) == 0
