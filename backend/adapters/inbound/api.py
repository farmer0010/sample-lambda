from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from backend.application.service import MemoService
from backend.adapters.outbound.dynamodb_repository import DynamoDBRepository
from backend.application.ports import MemoRepository

# 스프링의 @RestContrroler 역할을 할 라우터 생성
router = APIRouter()

# 스프링의 dto 역할
class MemoCreateRequest(BaseModel):
    content: str
    category: str = "cli"

def get_memo_service() -> MemoService:
    repo = DynamoDBRepository()
    return MemoService(repo)

@router.post("/v1/add")
def add_memo(request: MemoCreateRequest, service: MemoService = Depends(get_memo_service)):
    """메모를 저장하는 api 엔드 포인트"""

    try:
        memo = service.create_memo(content=request.content, category=request.category)
        return {"message" : "메모 저장 완료", "id" : memo.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

