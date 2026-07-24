import time

import requests

from cli.application.ports.outbound import AuthRepositoryPort


class GitHubDeviceAuthAdapter(AuthRepositoryPort):
    DEVICE_CODE_URL = "https://github.com/login/device/code"
    ACCESS_TOKEN_URL = "https://github.com/login/oauth/access_token"

    def __init__(self, client_id: str):
        self.client_id = client_id

    def request_device_code(self) -> dict:
        headers = {"Accept": "application/json"}
        payload = {
            "client_id": self.client_id,
            "scope": "read:user",
        }
        response = requests.post(
            self.DEVICE_CODE_URL, json=payload, headers=headers, timeout=5
        )
        response.raise_for_status()
        return response.json()

    def poll_for_token(self, device_code: str, interval: int = 5) -> dict:
        headers = {"Accept": "application/json"}
        payload = {
            "client_id": self.client_id,
            "device_code": device_code,
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
        }

        while True:
            time.sleep(interval)
            response = requests.post(
                self.ACCESS_TOKEN_URL, json=payload, headers=headers, timeout=5
            )
            data = response.json()

            if "access_token" in data:
                return data

            error = data.get("error")
            if error == "authorization_pending":
                continue
            elif error == "slow_down":
                interval += 5
            else:
                raise RuntimeError(f"Github 인증 실패: {error}")
