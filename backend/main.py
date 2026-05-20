from fastapi import FastAPI
from mangum import Mangum
from backend.adapters.inbound import api

app = FastAPI(
    title = "메모 API",
    description = "서버리스 메모 API",
)

app.include_router(api.router)

handler = Mangum(app)