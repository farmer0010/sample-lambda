import argparse

from cli.application.exceptions import (
    AuthDeviceFlowError,
    AuthenticationError,
)
from cli.dependencies import container


def main():
    parser = argparse.ArgumentParser(description="mylog CLI", add_help=False)
    parser.add_argument("-h", "--help", action="store_true", help="도움말 출력")

    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("login", help="깃허브 계정으로 로그인합니다.")
    subparsers.add_parser("logout", help="로그아웃합니다.")

    add_parser = subparsers.add_parser("add", help="새로운 메모를 기록합니다.")
    add_parser.add_argument("content", type=str, help="저장할 메모 내용")
    add_parser.add_argument(
        "-c", "--category", type=str, default=None, help="카테고리 지정"
    )

    list_parser = subparsers.add_parser("list", help="저장된 메모를 조회합니다.")
    list_parser.add_argument(
        "category", type=str, nargs="?", default=None, help="조회할 카테고리"
    )
    list_parser.add_argument(
        "-l", "--limit", type=int, default=5, help="출력 개수 지정"
    )

    update_parser = subparsers.add_parser("update", help="기존 메모를 수정합니다.")
    update_parser.add_argument("id", type=str, help="수정할 메모 고유 ID")
    update_parser.add_argument("content", type=str, help="새로운 내용")

    rm_parser = subparsers.add_parser("rm", help="메모를 삭제합니다.")
    rm_parser.add_argument("id", type=str, help="삭제할 메모 고유 ID")

    subparsers.add_parser("help", help="도움말 매뉴얼을 출력합니다.")

    args, unknown = parser.parse_known_args()

    if args.help or args.command == "help" or args.command is None:
        print("""Usage (사용 예시):

mylog [options]

Commands:
login      깃허브 계정으로 로그인하여 클라우드 환경을 연동합니다.
add        새로운 메모를 기록합니다. (-c 카테고리 지정)
list       저장된 메모를 조회합니다. (-l 개수)
update     기존 메모의 내용을 수정합니다. (ID 필요)
rm         저장된 메모를 삭제합니다. (ID 필요)
help       현재 화면의 도움말 매뉴얼을 출력합니다.""")
        return

    if args.command == "login":
        try:
            print("GitHub 서버에 로그인 요청 코드를 생성하는 중...")
            login_data = container.auth_service.request_login()

            print("\n" + "=" * 60)
            print("[GitHub 로그인 안내]")
            print("1. 웹 브라우저를 열고 다음 주소로 접속하세요.")
            print(f"   {login_data['verification_uri']}")
            print("2. 아래 코드를 입력하고 승인을 완료하세요.")
            print(f"   [ {login_data['user_code']} ]")
            print("=" * 60 + "\n")
            print("사용자의 브라우저 로그인을 기다리는 중입니다...")

            if container.auth_service.complete_login(
                login_data["device_code"], login_data["interval"]
            ):
                print("\n[로그인 성공]")
                print("깃허브 토큰이 안전하게 암호화 되어 저장되었습니다.")
            else:
                print("\n[로그인 실패] 깃허브 토큰을 획득하지 못했습니다.")
        except AuthDeviceFlowError as e:
            print(f"\n[로그인 실패] {e}")
        except Exception as e:
            print(f"로그인 예외 발생: {e}")

    elif args.command == "logout":
        try:
            if container.auth_service.logout():
                print("토큰이 안전하게 파기되었습니다. (로그아웃 성공)")
            else:
                print("이미 로그아웃된 상태거나 삭제할 토큰이 없습니다.")
        except Exception as e:
            print(f"로그아웃 실패: {e}")

    elif args.command == "add":
        try:
            container.memo_service.save_memo(
                content=args.content,
                category=args.category,
            )
            cat_title = args.category if args.category else "basic"
            print(f"\n> [{cat_title}] 메모가 저장되었습니다.")
        except AuthenticationError as e:
            print(f"\n[인증 실패] {e}")
        except Exception as e:
            print(f"\n[저장 실패] {e}")

    elif args.command == "list":
        try:
            memos = container.memo_service.get_memos(
                category=args.category,
                limit=args.limit,
            )

            cat_title = args.category if args.category else "전체"
            print(f"\n> [{cat_title}] 최근 메모 ({len(memos)}개 출력)")
            for m in memos:
                print(
                    f"  [ID: {m.get('id', 'N/A')}] "
                    f"{m.get('created_at', '')} | "
                    f"{m.get('content', '')}"
                )
        except AuthenticationError as e:
            print(f"\n[인증 실패] {e}")
        except Exception as e:
            print(f"\n[조회 실패] {e}")

    elif args.command == "update":
        try:
            container.memo_service.update_memo(
                memo_id=args.id,
                content=args.content,
            )
            print(f"\n> [{args.id}] 메모가 성공적으로 수정되었습니다.")
        except AuthenticationError as e:
            print(f"\n[인증 실패] {e}")
        except Exception as e:
            print(f"\n[수정 실패] {e}")

    elif args.command == "rm":
        try:
            container.memo_service.delete_memo(memo_id=args.id)
            print(f"\n> {args.id}번 메모가 깔끔하게 삭제되었습니다.")
        except AuthenticationError as e:
            print(f"\n[인증 실패] {e}")
        except Exception as e:
            print(f"\n[삭제 실패] {e}")


if __name__ == "__main__":
    main()
