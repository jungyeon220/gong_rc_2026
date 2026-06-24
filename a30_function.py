def print_hello(a : int, value: str) -> str:
    for i in range(a):
        print("안녕하세요!, value, i")
    return "execution OK!"
  

def main():
    re = print_hello(3, "Hi") # type hint, positional argument
    print(re)
  

if __name__ == "__main__":
    main()