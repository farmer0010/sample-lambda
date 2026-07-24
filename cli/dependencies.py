from cli.adapters.outbound.github_auth_adapter import GitHubDeviceAuthAdapter
from cli.adapters.outbound.http_memo_adapter import HttpMemoRepositoryAdapter
from cli.adapters.outbound.keyring_token_adapter import KeyringTokenAdapter
from cli.application.ports.inbound import AuthUseCase, MemoUseCase
from cli.application.service import AuthService, MemoService
from cli.config import settings


class Container:
    def __init__(self):
        self.token_storage = KeyringTokenAdapter()
        self.memo_repo = HttpMemoRepositoryAdapter(api_base_url=settings.API_BASE_URL)
        self.auth_repo = GitHubDeviceAuthAdapter(
            client_id=settings.GITHUB_CLIENT_ID,
        )

        self.memo_service: MemoUseCase = MemoService(
            memo_repo=self.memo_repo,
            token_storage=self.token_storage,
        )
        self.auth_service: AuthUseCase = AuthService(
            auth_repo=self.auth_repo,
            token_storage=self.token_storage,
        )


container = Container()
