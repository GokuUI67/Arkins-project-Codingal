import math
class Circle:
    def __init__(self, radius):
        self.radius = radius
    def area(self):
        return math.pi * self.radius ** 2
    def perimeter(self):
        return 2 * math.pi * self.radius
r = float(input("Enter The Radius of The Circle: "))
circle = Circle(r)
print(f"Area of The Circle: {circle.area():.2f}")