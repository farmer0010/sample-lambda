import argparse
import urllib.request
import json

API_URL = "https://4roukuec13.execute-api.ap-northeast-2.amazonaws.com/v1/add"

def send_to_aws


def main():
    parser = argparse.ArgumentParser(description="나만의 터미널 메모장")
    subparsers = parser.add_subparsers(dest="command", help="사용할 명령어를 입력하세요")

    add_parser = subparsers.add_parser("add", help="새로운 메모를 저장합니다.")
    add_parser.add_argument("content", type=str, help="저장할 메모 내용을 입력하세요")

    args = parser.parse_args()

    if args.command == "add":
        print(f"[명령어 인식 성공] 저장할 내용 : {args.content}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
