#1:

nums=[num for num in range(1500, 2701) if num % 35 == 0]
print(f"1: {nums}\n")

#2:

print("2:", end = " ")

def CelToFahr(cel):
    fahr = int(cel * 9 / 5 + 32)
    print(f"{cel}°C is {fahr} in Fahrenheit")

def FahrToCel(fahr):
    cel = int((fahr - 32) / 9 * 5)
    print(f"{fahr}°F is {cel} in Celcius")

CelToFahr(60)
print("  ", end = " ")
FahrToCel(45)