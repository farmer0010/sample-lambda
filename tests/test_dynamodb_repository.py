import boto3
from moto import mock_aws
from backend.domain.memo import Memo
from backend.adapters.outbound.dynamodb_repository import DynamoDBRepository
import pytest
from botocore.exceptions import ClientError

@mock_aws
def test_save_memo():
    dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
    test_table_name = 'test-memo-table'

    dynamodb.create_table(
        TableName=test_table_name,
        KeySchema=[
            {'AttributeName': 'PK', 'KeyType': 'HASH'},
            {'AttributeName': 'SK', 'KeyType': 'RANGE'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'PK', 'AttributeType': 'S'},
            {'AttributeName': 'SK', 'AttributeType': 'S'}
        ],
        BillingMode='PAY_PER_REQUEST'
    )
    repo = DynamoDBRepository(table_name=test_table_name)
    memo = Memo(content="테스트 코드 메모", category="test")
    repo.save(memo)

    table = dynamodb.Table(test_table_name)
    response = table.get_item(Key={"PK": f"MEMO#{memo.id}", "SK": memo.created_at})

    assert 'Item' in response
    assert response['Item']['content'] == "테스트 코드 메모"
    assert response['Item']['category'] == "test"

@mock_aws
def test_save_memo_table_not_exist():
    wrong_table_name = "not-exist-table"

    repo = DynamoDBRepository(table_name=wrong_table_name)
    memo = Memo(content="존재하지않는 테이블에 저장 시도", category="test")

    with pytest.raises(ClientError) as exc_info:
        repo.save(memo)

    assert "ResourceNotFoundException" in str(exc_info.value)