class A_test:
    def _repr__(self):
        return "A_test 객체이다."

def main():
    print("12345")
    print(123, "kim", "jeong", "yeon")
    print(3.12345)
    a = A_test()
    print(a)

    print("this is", "ptyhon", "class!!", sep="_", end=" ")
    print("this is", "python", "class!!", sep="_")
    

if __name__ == "__main__":
    main()