def print_n_time(value, n=2, v=3, g=5, *sum):
    sum_ = 0
    for i in range(n):
        print(value)
    for i in sum:
        sum_ += i
    return sum_

def main():
    print(print_n_time("안녕하세요", 10, 123, 54123, 123))
  
if __name__ == "__main__":
    main()