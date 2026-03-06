class A:
    def __init__(self, a):
        self.a = a 
    def __it__(self, other):
        if(self.a<other.a):
            return "OBJ1 IS LESS THAN OBJ2!!!!!"
    def __eq__(self, other):
        if(self.a == other.a):
            return "BOTH ARE EQUALLLL"
        else:
            return "NOT EQUALLLL"
obj1 = A(2)
obj2 = A(3)
print("PasESSSEd VALUUUUS: ", obj1.a, obj2.a)
print(obj1 < obj2)
obj3 = A(4)
obj4 = A(4)
print("PASSEESEDD VALIUUUUS: ", obj3.a, obj4.a)
print(obj3 == obj4)