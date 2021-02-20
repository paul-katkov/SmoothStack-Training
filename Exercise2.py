#1:

a=50+50
b=100-10
print(f"1: {a+b}\n")

#2:

print(f"2: {30+6,6^6,6**6,6+6+6+6+6+6}\n")

#3:

print("3: Hello World")
print("   Hello World : 10\n")

#4:

# Formula Solution:

print("4: Formula Solution:")

import math # For ceiling function

P, R, L = input().split()
P, R, L = [int(P), int(R), int(L)]

print(f"{math.ceil(P * R / 12 / 100 / (1 - pow(1 + R / 12 / 100, -L)))}\n")

# Recursion Solution:

print("   Recursion Solution:")

P, R, L = input().split()
P, R, L = [int(P), int(R), int(L)]

def monthly_payment(init_loan, int_rate_month, monthly_pay, month_num):
    month_num += 1
    init_loan = init_loan * (100 + int_rate_month) / 100 - monthly_pay

    if init_loan <= 0:
        return month_num
    else:
        return monthly_payment(init_loan, int_rate_month, monthly_pay, month_num)
    if month_num > 1199: # Cap the recursion at 100 years
        return month_num
        print("ERROR: Recursion cap reached (1200)")

Rm = R / 12 # Monthly interest rate
min_monthly_pay = int (P / L) # Assuming interest rate cannot be negative
max_monthly_pay = P # Arbitrary max

output = min_monthly_pay
for monthly_pay in range(min_monthly_pay, max_monthly_pay):
    if monthly_payment(P, Rm, monthly_pay, 0) == L:
        output = monthly_pay
        break

print(output)