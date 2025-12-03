Medico = int(input("Did You Have A Medical Cause Pls Enter Y or N: "))
Atten = int(input("Enter The Attendence You Have Currently:  "))
if Medico == 'Y':
    print("You Are Allowed")
else:
    if Atten >= 75:
        print("Allowed")
    else:
        print("NOT ALLOWEDDDDD!!!!!")