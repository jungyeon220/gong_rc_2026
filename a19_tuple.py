def main():
    tu = tuple()
    print(tu, type(tu))
    tu = (1, 2)
    print(tu, type(tu))
    print(tu[0])
    for ele in tu:
        print(ele)

    tu_1 = 1, 2
    print(tu_1, type(tu_1))
    a = 10
    b = 20
    # swap C 스타일
    tmp = a
    a = b
    b = tmp
    # swap python 스타일
    a, b = b, a
    print(a, b)

if __name__ == "__main__":
    main()