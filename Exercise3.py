#1:

print("1: " + "Hello World"[8] + "\n") # Problem number and '\n' for terminal screenshot readability

#2:

print("2: " + "thinker"[2:5] + "\n")

#3:

print("3: " + "Sammy"[2:] + "\n")

#4:

print("4: " + "".join(set("Mississippi")) + "\n")

#5:

num = int(input())
lines = []

for i in range(num):
    line = "".join(char for char in input() if char.isalnum())
    lines += [line.lower()]

for line in lines:
    if line == line[::-1]:
        print("Y", end = " ")
    else:
        print("N", end = " ")