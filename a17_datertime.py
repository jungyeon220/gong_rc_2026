import datetime

from a01_hello import main as hello_main


def main():
    now = datetime.datetime.now()

    if 9 < now.hour < 12:
        print(f"현재 시간은 {now.hour}시로 오전입니다.")
    elif 0 <= now.hour < 9:
        print(f"현재 시간은 {now.hour}시로 새벽입니다.")
    else:
        print(f"현재 시간은 {now.hour}시로 오후입니다.")


    print(now.month, type(now.month))
    
    # 봄, 여름, 가을, 겨울을 출력하세요
    # 12, 1, 2, 3 -> 겨울
    # 4, 5 -> 봄
    # 6, 7, 8 -> 여름
    # 9, 10, 11 -> 가을

    if now.month in [12, 1, 2, 3]:
        print("겨울입니다.")
    elif now.month in [4, 5]:
        print("봄입니다.")
    elif now.month in [6, 7, 8]:
        print("여름입니다.")
    else:
        print("가을입니다.")


if __name__ == "__main__":
    main()