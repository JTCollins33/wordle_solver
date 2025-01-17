payments=[100,200,300,400,500,600,700,800, 900, 1000]
for MONTHLY_PAYMENT in payments:
    RATE = 3.89
    MONTHLY_RATE=(RATE/100)/12
    # MONTHLY_PAYMENT=700
    LOAN_AMOUNT=10000

    total_paid=0
    n_months=0

    while(LOAN_AMOUNT>0):
        month_interest = MONTHLY_RATE*LOAN_AMOUNT

        principal_paid = MONTHLY_PAYMENT-month_interest

        LOAN_AMOUNT-=principal_paid
        total_paid+=MONTHLY_PAYMENT
        n_months+=1
    
    total_paid+=LOAN_AMOUNT

    print("Monthly rate: ", MONTHLY_PAYMENT, "\tTotal Paid: $", int(total_paid), "\tTotal months: ", n_months, "\n\n")