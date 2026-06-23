def main():
    ptime = datetime.datetime.now()
    list_a = [0, 1, 2, 3, 4, 5, 6]
    list_b = ["a", "b", "c", "d", "e", "f", ptime]
    del list_a[0]
    del list_b[2]
    del list_b[5]
    del ptime
    print(list_a)
    print(list_b)
    print(ptime)

    if __name__ == "__main__":
        main()
        