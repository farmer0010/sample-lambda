import boto3
from backend.domain.memo import Memo
from backend.application.ports import MemoRepository

class DynamoDBRepository(MemoRepository):
    def __init__(self, table_name: str):
        self.dynamodb = boto3.resource("dynamodb",
                                       region_name="ap-northeast-2")
        self.table = self.dynamodb.Table(table_name)

    def save(self, memo: Memo) -> None:

        item = {
            'PK': f"MEMO#{memo.id}",
            'SK': memo.created_at,
            'category': memo.category,
            'content': memo.content,
            'created_at': memo.created_at,
        }
        self.table.put_item(Item=item)

    def get_all(self) -> list[Memo]:
        pass