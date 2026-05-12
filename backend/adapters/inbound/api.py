from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from backend.adapters.outbound.dynamodb_repository import DynamoDBRepository
from backend.application.service import MemoService
from backend.domain.memo import MemoDomainError

router = APIRouter()

class MemoCreateRequest(BaseModel):
    content: str
    category: str | None = None

class MemoCreateResponse(BaseModel):
    message: str
    id: str

def get_memo_service() -> MemoService:
    repo = DynamoDBRepository()
    return MemoService(repo)

@router.post("/v1/add", response_model=MemoCreateResponse)
def add_memo(
    request: MemoCreateRequest, service: MemoService = Depends(get_memo_service)
):
    try:
        memo = service.create_memo(content=request.content, category=request.category)
        return MemoCreateResponse(message="메모 저장 완료", id=memo.id)
    except MemoDomainError as e:
        raise HTTPException(status_code=400, detail=str(e))