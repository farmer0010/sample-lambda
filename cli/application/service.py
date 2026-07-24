from cli.application.exceptions import AuthDeviceFlowError, AuthenticationError
from cli.application.ports.inbound import AuthUseCase, MemoUseCase
from cli.application.ports.outbound import (
    AuthRepositoryPort,
    MemoRepositoryPort,
    TokenStoragePort,
)


class MemoService(MemoUseCase):
    def __init__(self, memo_repo: MemoRepositoryPort, token_storage: TokenStoragePort):
        self.memo_repo = memo_repo
        self.token_storage = token_storage

    def _require_token(self) -> str:
        token = self.token_storage.get_token()
        if not token:
            raise AuthenticationError(
                "유효한 로그인 정보가 없습니다.\n"
                "'mylog login' 명령어를 실행해 다시 로그인해 주세요."
            )
        return token

    def save_memo(self, content: str, category: str | None = None) -> dict:
        token = self._require_token()
        return self.memo_repo.save(token=token, content=content, category=category)

    def get_memos(self, category: str | None = None, limit: int = 5) -> list:
        token = self._require_token()
        return self.memo_repo.get_all(token=token, category=category, limit=limit)

    def update_memo(self, memo_id: str, content: str) -> dict:
        token = self._require_token()
        return self.memo_repo.update(memo_id=memo_id, token=token, content=content)

    def delete_memo(self, memo_id: str) -> dict:
        token = self._require_token()
        return self.memo_repo.delete(memo_id=memo_id, token=token)


class AuthService(AuthUseCase):
    def __init__(self, auth_repo: AuthRepositoryPort, token_storage: TokenStoragePort):
        self.auth_repo = auth_repo
        self.token_storage = token_storage

    def request_login(self) -> dict:
        try:
            device_data = self.auth_repo.request_device_code()
            return {
                "user_code": device_data.get("user_code"),
                "verification_uri": device_data.get("verification_uri"),
                "device_code": device_data.get("device_code"),
                "interval": device_data.get("interval", 5),
            }
        except Exception as e:
            raise AuthDeviceFlowError(f"깃허브 로그인 요청 실패: {e}") from e

    def complete_login(self, device_code: str, interval: int) -> bool:
        try:
            token_data = self.auth_repo.poll_for_token(
                device_code=device_code,
                interval=interval,
            )
            access_token = token_data.get("access_token")

            if access_token:
                self.token_storage.save_token(access_token)
                return True
            return False
        except Exception as e:
            raise AuthDeviceFlowError(str(e)) from e

    def logout(self) -> bool:
        return self.token_storage.delete_token()
