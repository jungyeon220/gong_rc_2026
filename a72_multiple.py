class Person:
    def __init__(self, b):
        self.b = b

        def greeting(self):
            print("안녕하새요")

class University:
    def __init__(self, a):
        self.a = a

        def greeting(self):
            print("학점 관리")

        

class Undergraduate(Person, University):
    def __init__(self, c):
        Person.__init__(self, 2)
        University.__init__(seld, 1)
        self.c = c

def main():
    kim = Undergraduate (3)
    print(kim.a, kim.b, kim.c)
    kim.greeting()
    kim.massage_credit()
    print(Undergraduate.__mro__)

if __name__ == "__main__":
    main() 