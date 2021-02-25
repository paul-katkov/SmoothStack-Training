import numpy as np
import pandas as pd

df = pd.read_csv("Salaries.csv", sep = ",", low_memory = False)

#1:

print(f"1: {list(df.columns)}\n")

#2:

print(f"2: {len(df.index)}\n")

#3:

print(f"3: {round(pd.to_numeric(df['BasePay'][df['Id'] < 10001]).mean(), 2)}\n")

#4:

print(f"4: {df['TotalPayBenefits'].max()}\n")

#5:

print(f"5: {df['JobTitle'][df['EmployeeName'] == 'JOSEPH DRISCOLL'].values[0]}\n")

#6:

print(f"6: {df['TotalPay'][df['EmployeeName'] == 'JOSEPH DRISCOLL'].values[0]}\n")

#7:

print(f"7: {df['EmployeeName'][df['TotalPay'] == df['TotalPay'].max()].values[0]}\n")

#8:

print(f"8: {df['EmployeeName'][df['TotalPay'] == df['TotalPay'].min()].values[0]}")
print(f"   Their pay is {df['TotalPay'].min()}, which is negative...\n")

#9:

print("9:")
print(round(df.groupby('Year')['TotalPay'].mean(), 2))
print("")

#10:

print(f"10: {len(df['JobTitle'].unique())}\n")

#11:

print("11:")
print(df['JobTitle'].value_counts().head(7))
print("")

#12:

print(f"12: {len(df['JobTitle'][df['Year'] == 2013].value_counts()[df['JobTitle'][df['Year'] == 2013].value_counts() == 1])}\n")

#13:

print(f"13: {len(df[df['JobTitle'].str.contains('Chief')])}\n")

#14:

print(f"14: (No Correlation) {df['TotalPay'].groupby(df['JobTitle'].str.len()).mean()}")