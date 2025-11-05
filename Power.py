base = int(input("Enter The Base: "))
exponet = int(input("Enter The Exponet: "))
result = 1
for _ in range(exponet):
    result *= base
print(f"{base} Raised to the power of {exponet} is {result}")