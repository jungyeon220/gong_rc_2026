import math

class Circle:
    def __init__(self, radius):
        self.__radius = radius

    def get_circumference(self):
        return 2* math.pi * self.__radius
    def get_area(self):
        return math.pi * (self.__radius) ** 2
    
    @property
    def radius(self):
        self.__radius = radius

    @radius.setter
    def radius(slef, value):
        self.__radius = vlaue
        


class Rectangle(Circle):
    def __init__(self, radius):
        super().__init__(5)
        self.__radius = radius
def print_c():
    print("원의 둘레와 넓이를 구합시다.")
    print(f"원의 둘레: {c.get_circumference():.2f}")
    print(f"원의 넓이: {c.get_area():.2f}")

def main():
    c = Circle(5)
    print(c.__dict__)
    print(c._Circle__radius)
    r = Rectangle(6)
    print(r.__dict__)
    # __변수는 overriding 을 방지하는 맹글링기능이다

  
    print_c(c)
    c.radius = 10
    print(c.radius)
    print_c(c)


if __name__ == "__main__":
    main()   