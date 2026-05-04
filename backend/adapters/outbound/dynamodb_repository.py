import boto3
from backend.domain.memo import Memo
from backend.application.ports import MemoRepository

class DynamoDBRepository(MemoRepository):
    def __init__(self, table_name: str = "juyo-serverless-dev-table"):
        self.dynamodb = boto3.resource("dynamodb",
                                       region_name="ap-northeast-2")
        self.table = self.dynamodb.Table(table_name)

    def save(self, memo: Memo) -> None:
        """포트의 save 규칙을 구현"""

        item = {
            'id': memo.id,
            'category': memo.category,
            'content': memo.content,
            'created_at': memo.created_at,
        }
        self.table.put_item(Item=item)

    def get_all(self) -> list[Memo]:
        """조회 기능은 나중에 list 만들 떄 구현해둘 예정"""
        pass