import os

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from backend.adapters.outbound.dynamodb_repository import DynamoDBRepository
from backend.application.ports import MemoUseCase
from backend.application.service import MemoService
from backend.domain.memo import MemoDomainError

router = APIRouter()


class MemoCreateRequest(BaseModel):
    content: str
    category: str | None = None


class MemoCreateResponse(BaseModel):
    message: str
    id: str


def get_memo_use_case() -> MemoUseCase:
    table_name = os.getenv("DYNAMODB_TABLE")
    if not table_name:
        raise ValueError("DYNAMODB_TABLE 환경변수가 설정되지 않았습니다")

    repo = DynamoDBRepository(table_name=table_name)
    return MemoService(repo)


@router.post("/add", response_model=MemoCreateResponse)
def add_memo(
    request: MemoCreateRequest, use_case: MemoUseCase = Depends(get_memo_use_case)
):
    try:
        memo = use_case.create_memo(content=request.content, category=request.category)
        return MemoCreateResponse(message="메모 저장 완료", id=memo.id)
    except MemoDomainError as e:
        raise HTTPException(status_code=400, detail=str(e))
