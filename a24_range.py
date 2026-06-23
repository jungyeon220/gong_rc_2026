def main():
    print(range(10))
    print(list(range(0, 10, 1)))
    a = range(10)
    print(list(a))
    print(list(range(5, 10, 3)))
    a = []
    for i in range(0, 100, 1):
        a.append(i+1)
    print(a) 

    a = [i+1 for i in range(100)]   
    print(a)

    list_b = ["a", "b", "c", "d", "e", "f"]
    for a, ele in enumerate(list_b):
        print(ele+ "원소", a)

    list_c = ["에이", "비", "씨", "디", "이", "에프"]
    for i in range(6):
        print(list_b[i], list_c[i])
    for b, c in zip(list_b, list_c):
        print(b, c)
        

if __name__ == "__main__":
    main()