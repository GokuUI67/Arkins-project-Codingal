def Total_Calc(bill_amount,tip_perc):

    total = bill_amount*(1 + 0.01*tip_perc)
    totl = round(total,2)
    print(f"Pleaseeeeeeee PAYYYYYYYYYYYYYYYYYYYYY ${total}")


Total_Calc(150,20)