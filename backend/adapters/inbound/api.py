import os

from fastapi import APIRouter, Depends, Header, HTTPException
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
    request: MemoCreateRequest,
    x_user_id: str = Header(..., alias="X-USER-ID"),
    use_case: MemoUseCase = Depends(get_memo_use_case),
):
    try:
        memo = use_case.create_memo(
            user_id=x_user_id, content=request.content, category=request.category
        )
        return MemoCreateResponse(message="메모 저장 완료", id=memo.id)
    except MemoDomainError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/memos")
def get_memos(
    category: str | None = None,
    limit: int = 5,
    x_user_id: str = Header(..., alias="X-USER-ID"),
    service: MemoUseCase = Depends(get_memo_use_case),
):
    memos = service.get_all_memos(user_id=x_user_id, category=category, limit=limit)
    return {"memos": memos}


@router.get("/memos/{memo_id}")
def get_memo(
    memo_id: str,
    service: MemoUseCase = Depends(get_memo_use_case),
):
    memo = service.get_memo_by_id(memo_id)
    if not memo:
        raise HTTPException(status_code=404, detail="메모를 찾을 수 없습니다")
    return memo
