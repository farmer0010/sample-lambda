import keyring

from cli.application.ports.outbound import TokenStoragePort


class KeyringTokenAdapter(TokenStoragePort):
    def __init__(
        self, service_name: str = "mylog-app", username: str = "user_secure_token"
    ):
        self.service_name = service_name
        self.username = username

    def get_token(self) -> str | None:
        return keyring.get_password(self.service_name, self.username)

    def save_token(self, token: str) -> None:
        keyring.set_password(self.service_name, self.username, token)

    def delete_token(self) -> bool:
        try:
            keyring.delete_password(self.service_name, self.username)
            return True
        except keyring.errors.PasswordDeleteError:
            return False
