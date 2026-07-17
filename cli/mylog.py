import argparse
import os
import time

import keyring
import requests
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")

KEYRING_SERVICE_NAME = "mylog-app"
KEYRING_TOKEN_KEY = "user_secure_token"


def get_saved_token() -> str | None:
    return keyring.get_password(KEYRING_SERVICE_NAME, KEYRING_TOKEN_KEY)


def save_token(token: str):
    keyring.set_password(KEYRING_SERVICE_NAME, KEYRING_TOKEN_KEY, token)


def delete_token():
    try:
        keyring.delete_password(KEYRING_SERVICE_NAME, KEYRING_TOKEN_KEY)
        print("토큰이 안전하게 파기되었습니다. (로그아웃 성공)")
    except keyring.errors.PasswordDeleteError:
        print("이미 로그아웃된 상태거나 삭제할 토큰이 없습니다.")


def send_to_aws(content):
    if not API_BASE_URL:
        print("에러: 환경변수에 API_BASE_URL이 설정되어 있지 않습니다.")
        return

    url = f"{API_BASE_URL}/memos"
    payload = {
        "category": "basic",
        "content": content,
    }

    headers = {
        "Content-Type": "application/json",
    }

    token = get_saved_token()
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=5,
        )

        if response.status_code == 401:
            print("[인증 실패] 유효한 로그인 정보가 없거나 만료되었습니다.")
            print("'mylog login' 명령어를 실행해 다시 로그인해 주세요.")
            return

        response.raise_for_status()
        result = response.json()

        print("[AWS 저장 성공]")
        print(f"서버의 응답 메시지: {result.get('message', '성공')}")
        print(f"저장된 고유 ID (ULID): {result.get('id')}")

    except requests.exceptions.Timeout:
        print("에러: 서버 응답 시간이 초과되었습니다. 인터넷 연결을 확인해주세요.")
    except Exception as e:
        print(f"서버 통신 중 에러 발생: {e}")


def handle_login():
    if not GITHUB_CLIENT_ID:
        print("에러: 환경변수에 GITHUB_CLIENT_ID가 설정되어 있지 않습니다.")
        return

    print("GitHub 서버에 로그인 요청 코드를 생성하는 중...")

    device_code_url = "https://github.com/login/device/code"
    headers = {
        "Accept": "application/json",
    }
    payload = {
        "client_id": GITHUB_CLIENT_ID,
        "scope": "read:user",
    }

    try:
        res = requests.post(
            device_code_url,
            json=payload,
            headers=headers,
            timeout=5,
        )
        res.raise_for_status()
        res_data = res.json()
    except Exception as e:
        print(f"깃허브 로그인 요청에 실패했습니다: {e}")
        return

    device_code = res_data.get("device_code")
    user_code = res_data.get("user_code")
    verification_uri = res_data.get("verification_uri")
    interval = res_data.get("interval", 5)

    print("\n" + "=" * 60)
    print("[GitHub 로그인 안내]")
    print("1. 웹 브라우저를 열고 다음 주소로 접속하세요.")
    print(f"   {verification_uri}")
    print("2. 아래 코드를 입력하고 승인을 완료하세요.")
    print(f"   [ {user_code} ]")
    print("=" * 60 + "\n")

    token_url = "https://github.com/login/oauth/access_token"
    token_payload = {
        "client_id": GITHUB_CLIENT_ID,
        "device_code": device_code,
        "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
    }

    print("사용자의 브라우저 로그인을 기다리는 중입니다...")

    while True:
        try:
            res_token = requests.post(
                token_url,
                json=token_payload,
                headers=headers,
                timeout=5,
            )
            res_token.raise_for_status()
            token_data = res_token.json()

            error = token_data.get("error")
            if error:
                if error == "authorization_pending":
                    time.sleep(interval)
                    continue
                elif error == "slow_down":
                    interval += 5
                    time.sleep(interval)
                    continue
                elif error == "expired_token":
                    print("로그인 제한 시간이 만료되었습니다. 다시 시도해 주세요.")
                    return
                else:
                    print(f"로그인 중 에러 발생: {token_data.get('error_description')}")
                    return

            github_access_token = token_data.get("access_token")
            break

        except Exception as e:
            print(f"대기 중 에러 발생: {e}")
            return

    if not github_access_token:
        print("깃허브 토큰을 획득하지 못했습니다.")
        return

    save_token(github_access_token)
    print("\n[로그인 성공]")
    print("깃허브 토큰이 안전하게 암호화 되어 저장되었습니다.")


def main():
    parser = argparse.ArgumentParser(description="터미널 메모장")
    subparsers = parser.add_subparsers(
        dest="command",
        help="사용할 명령어를 입력하세요",
    )

    subparsers.add_parser(
        "login",
        help="깃허브 계정으로 안전하게 로그인합니다.",
    )

    subparsers.add_parser(
        "logout",
        help="키체인에서 로그인 정보를 삭제합니다.",
    )

    add_parser = subparsers.add_parser(
        "add",
        help="새로운 메모를 저장합니다.",
    )
    add_parser.add_argument(
        "content",
        type=str,
        help="저장할 메모 내용을 입력하세요",
    )

    args = parser.parse_args()

    if args.command == "login":
        handle_login()
    elif args.command == "logout":
        delete_token()
    elif args.command == "add":
        if not get_saved_token():
            print("\n[인증 필요] 이 명령어를 사용하려면 로그인이 필요합니다.")
            print("먼저 'mylog login'을 실행해 주세요.\n")
            return

        print(f"입력하신 '{args.content}' 문장을 클라우드로 전송합니다.")
        send_to_aws(args.content)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
