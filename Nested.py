string = input("Please enter your own word : ")

#take input of a character

char = input("Please enter your own Character : ")
i = 0
count = 0
while(i<len(string)):
    if (string[i]==char):
        count = count + 1
    i = i+1
print("Number of time it occurs is: ", count)