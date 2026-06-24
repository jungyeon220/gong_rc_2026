def test():
    print("함수가 호출 되었습니다.")
    yield "re"


def main():
    ge = test()     #함수의 실행이 매변 다른 결과를 요구할때
    print(ge)       
    # print(ge.__next__())
    print(next(ge))
    for re in ge:
        print(re)

if __name__ == "__main__":
    main()
