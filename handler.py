from mangum import Mangum
from app.main import app

# API Gateway의 요청을 FastAPI(app)로 전달해주는 어댑터입니다.
handler = Mangum(app)