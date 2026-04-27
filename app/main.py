import uuid
import boto3
from fastapi import FastAPI
from pydantic import BaseModel
from app.config import config

app = FastAPI()

dynamodb = boto3.resource("dynamodb", region_name='ap-northeast-2')
table_name = config.get('DYNAMODB_TABLE_NAME')
table = dynamodb.Table(table_name) if table_name else None


class MemoRequest(BaseModel):
    category: str = "basic"
    content: str

@app.post("/add")
def add_memo(request: MemoRequest):
    memo_id = str(uuid.uuid4())[:8]
    item = {
        "PK": "USER#juyo",
        "SK": f"MEMO#{memo_id}",
        "category": request.category,
        "content": request.content
    }
    table.put_item(Item=item)  #  aws db 저장

    return {
        "message": "메모 저장 완료",
        "id" : memo_id,
        "data" : item
    }

@app.get("/health")
def health():
    return {"status": "ok", "table": table_name}

