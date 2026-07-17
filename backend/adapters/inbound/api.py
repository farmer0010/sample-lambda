import requests
from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel

from backend.application.exceptions import MemoAccessDeniedError
from backend.application.ports import MemoUseCase
from backend.dependencies import get_memo_use_case
from backend.domain.memo import MemoDomainError

router = APIRouter()


class MemoCreateRequest(BaseModel):
    content: str
    category: str | None = None


class MemoCreateResponse(BaseModel):
    message: str
    id: str


class UpdateMemoRequest(BaseModel):
    content: str


def get_current_user_id(authorization: str | None = Header(None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="인증되지 않은 요청입니다. 유효한 Bearer 인증 토큰이 필요합니다.",
        )

    token = authorization.split(" ")[1]
    github_user_uri = "https://api.github.com/user"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }

    try:
        response = requests.get(github_user_uri, headers=headers, timeout=5)

        if response.status_code != 200:
            raise HTTPException(
                status_code=401, detail="유효하지 않거나 만료된 깃허브 토큰입니다."
            )

        user_data = response.json()
        return str(user_data.get("id"))

    except requests.exceptions.RequestException:
        raise HTTPException(
            status_code=503, detail="깃허브 인증 서버와 통신할 수 없습니다."
        )


@router.post("/memos", response_model=MemoCreateResponse)
def add_memo(
    request: MemoCreateRequest,
    user_id: str = Depends(get_current_user_id),
    use_case: MemoUseCase = Depends(get_memo_use_case),
):
    try:
        memo = use_case.create_memo(
            user_id=user_id,
            content=request.content,
            category=request.category,
        )
        return MemoCreateResponse(message="메모 저장 완료", id=memo.id)
    except MemoDomainError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/memos")
def get_memos(
    category: str | None = None,
    limit: int = 5,
    user_id: str = Depends(get_current_user_id),
    service: MemoUseCase = Depends(get_memo_use_case),
):
    memos = service.get_all_memos(
        user_id=user_id,
        category=category,
        limit=limit,
    )
    return {"memos": memos}


@router.get("/memos/{memo_id}")
def get_memo(
    memo_id: str,
    user_id: str = Depends(get_current_user_id),
    service: MemoUseCase = Depends(get_memo_use_case),
):
    memo = service.get_memo_by_id(
        memo_id=memo_id,
        user_id=user_id,
    )

    if not memo:
        raise HTTPException(status_code=404, detail="메모를 찾을 수 없습니다")

    return memo


@router.put("/memos/{memo_id}")
def update_memo(
    memo_id: str,
    request: UpdateMemoRequest,
    user_id: str = Depends(get_current_user_id),
    service: MemoUseCase = Depends(get_memo_use_case),
):
    try:
        updated_memo = service.update_memo(
            memo_id=memo_id,
            user_id=user_id,
            content=request.content,
        )
        return updated_memo

    except MemoAccessDeniedError as e:
        raise HTTPException(status_code=403, detail=str(e))

    except MemoDomainError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/memos/{memo_id}")
def delete_memo(
    memo_id: str,
    user_id: str = Depends(get_current_user_id),
    service: MemoUseCase = Depends(get_memo_use_case),
):
    try:
        service.delete_memo(memo_id=memo_id, user_id=user_id)
        return {"message": "메모 삭제 완료"}
    except MemoAccessDeniedError as e:
        raise HTTPException(status_code=403, detail=str(e))
