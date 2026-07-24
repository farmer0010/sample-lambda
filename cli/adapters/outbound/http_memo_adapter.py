import requests

from cli.application.ports.outbound import MemoRepositoryPort


class HttpMemoRepositoryAdapter(MemoRepositoryPort):
    def __init__(self, api_base_url: str):
        self.api_base_url = api_base_url

    def _get_headers(self, token: str) -> dict:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }

    def save(self, token: str, content: str, category: str | None = None) -> dict:
        url = f"{self.api_base_url}/memos"
        response = requests.post(
            url,
            json={"content": content, "category": category},
            headers=self._get_headers(token),
            timeout=5,
        )
        response.raise_for_status()
        return response.json()

    def get_all(self, token: str, category: str | None = None, limit: int = 5) -> list:
        url = f"{self.api_base_url}/memos"
        params: dict[str, str | int] = {"limit": limit}
        if category:
            params["category"] = category

        response = requests.get(
            url, headers=self._get_headers(token), params=params, timeout=5
        )

        response.raise_for_status()
        data = response.json()

        if isinstance(data, dict) and "memos" in data:
            return data["memos"]
        return data if isinstance(data, list) else []

    def update(self, memo_id: str, token: str, content: str) -> dict:
        url = f"{self.api_base_url}/memos/{memo_id}"
        response = requests.put(
            url, json={"content": content}, headers=self._get_headers(token), timeout=5
        )
        response.raise_for_status()
        return response.json()

    def delete(self, memo_id: str, token: str) -> dict:
        url = f"{self.api_base_url}/memos/{memo_id}"
        response = requests.delete(url, headers=self._get_headers(token), timeout=5)
        response.raise_for_status()
        return response.json()
