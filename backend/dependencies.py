import os

from backend.adapters.outbound.dynamodb_repository import DynamoDBRepository
from backend.application.ports import MemoUseCase
from backend.application.service import MemoService


def get_memo_use_case() -> MemoUseCase:
    table_name = os.getenv("DYNAMODB_TABLE")
    if not table_name:
        raise ValueError("DYNAMODB_TABLE 환경 변수가 설정되지 않았습니다.")

    repo = DynamoDBRepository(table_name=table_name)
    return MemoService(repo)
