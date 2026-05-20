import pytest
from unittest.mock import patch, MagicMock
from botocore.exceptions import ClientError

from backend.domain.memo import Memo
from backend.adapters.outbound.dynamodb_repository import DynamoDBRepository


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