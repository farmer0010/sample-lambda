import argparse
import requests

BASE_URL = "https://4roukuec13.execute-api.ap-northeast-2.amazonaws.com/v1"


def add_memo(content: str, category: str):
    """AWS 서버에 메모를 저장 요청합니다."""
    url = f"{BASE_URL}/add"
    payload = {"content": content, "category": category}

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # 200번대 응답이 아니면 에러처리
        result = response.json()
        print(
            f"> [{category}] 메모가 클라우드에 저장되었습니다. (ID: {result.get('id')})"
        )
    except requests.exceptions.RequestException as e:
        print(f"서버와의 통신에 실패했습니다. \n에러:{e}")


def list_memos(category: str, limit: int, search: str):
    """AWS서버에 메모를 조회하고 요청하고 출력합니다"""
    url = f"{BASE_URL}/memos"

    params = {"limit": limit}
    if category:
        params["category"] = category
    if search:
        params["search"] = search

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        memos = response.json().get("memos", [])

        if not memos:
            print("> 클라우드에 저장된 메모가 없습니다.")
            return

        print(f"> 최근 클라우드메모 ({len(memos)}개 출력)")
        for memo in memos:
            date_str = memo.get("created_at", "")[2:10].replace("-", ".")
            print(
                f"  [ID: {memo['id']}] [{memo['category']}] "
                f"{date_str} | {memo['content']}"
            )

    except requests.exceptions.RequestException as e:
        print(f"메모 조회에 실패했습니다. \n에러: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="개발자 전용 CLI 메모장 MyLog"
    )
    subparsers = parser.add_subparsers(dest="command", help="사용할 명령어")

    # 명령어 1. add
    parser_add = subparsers.add_parser("add", help="새로운 메모를 기록합니다.")
    parser_add.add_argument("content", type=str, help="저장할 메모 내용")
    parser_add.add_argument(
        "-c",
        "--category",
        type=str,
        default="basic",
        help="카테고리 지정 (기본값: basic)",
    )

    # 명령어 2. list
    parser_list = subparsers.add_parser("list", help="저장된 메모를 조회합니다.")
    parser_list.add_argument(
        "category", type=str, nargs="?", default=None, help="특정 카테고리만 조회"
    )
    parser_list.add_argument(
        "-l", "--limit", type=int, default=5, help="출력할 메모 개수"
    )
    parser_list.add_argument(
        "-s", "--search", type=str, default=None, help="검색어 포함 내용 찾기"
    )

    args = parser.parse_args()

    if args.command == "add":
        add_memo(args.content, args.category)
    elif args.command == "list":
        list_memos(args.category, args.limit, args.search)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
