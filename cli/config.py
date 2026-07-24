import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    def __init__(self):
        self.API_BASE_URL = os.getenv("API_BASE_URL")
        self.GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")

        self.validate()

    def validate(self):
        if not self.API_BASE_URL:
            raise EnvironmentError(
                "에러: 환경변수 API_BASE_URL이 설정되어 있지 않습니다"
            )
        if not self.GITHUB_CLIENT_ID:
            raise EnvironmentError(
                "에러: 환경변수 GITHUB_CLIENT_ID가 설정되어 있지 않습니다."
            )


settings = Settings()
