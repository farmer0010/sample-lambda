import argparse
import json
import urllib.request

API_URL = "https://4roukuec13.execute-api.ap-northeast-2.amazonaws.com/v1/add"


def send_to_aws(content):
    payload = {"category": "cli", "content": content}
    json_data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        url=API_URL, data=json_data, headers={"content-type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            print("[aws 저장 성공]")
            print(f"서버의 응답 메시지: {result['message']}")
            print(f"저장된 고유 ID: {result['id']}")
    except Exception as e:
        print(f"서버 통신중 에러 발생: {e}")


def main():
    parser = argparse.ArgumentParser(description="나만의 터미널 메모장")
    subparsers = parser.add_subparsers(
        dest="command", help="사용할 명령어를 입력하세요"
    )

    add_parser = subparsers.add_parser("add", help="새로운 메모를 저장합니다.")
    add_parser.add_argument("content", type=str, help="저장할 메모 내용을 입력하세요")

    args = parser.parse_args()

    if args.command == "add":
        print(f"입력하신 '{args.content} 문장을 클라우드로 전송'")
        send_to_aws(args.content)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
