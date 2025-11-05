char = input("Enter a Single Character: ")
if len(char) == 1 and char.isalpha():
    print(f"'{char}' is an Alphabet")
else:
    print(f"'{char}' is not an Alphabet")