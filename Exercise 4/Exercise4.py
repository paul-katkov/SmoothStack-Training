#1:

list1 = [7, "seven", 7.0]
print(f"1: {list1}\n")

#2:

list2 = [1, [1, 2]] # Problem states '[1, 1[1, 2]]' - assuming typo
print(f"2: {list2[1][1]}\n")

#3:

list3 = ['a', 'b', 'c']
print(f"3: {list3[1:]}\n")

#4:

dict1 = {"Monday":1, "Tuesday":2, "Wednesday":3, "Thursday":4, "Friday":5, "Saturday":6, "Sunday":7}

#5:

dict2 = {'k1':[1, 2, 3]}
print(f"4: {dict2['k1'][1]}\n")

#6:

list4 = [1, [2, 3]]
tupl1 = tuple(list4)

#7:

Mips = set("Mississippi")

#8:

Mips.add('X')

#9:

set1 = {1, 1, 2, 3}
print(f"10: {set1}\n")

#Question 1:

numline = ""

for i in range(2000, 3201):
    if i % 7 == 0 and i % 5 != 0:
        numline += (f"{i}, ")

numline = numline[:-2] # To remove ", " at the end

print(f"Q1: {numline}\n")

#Question 2:

num = int(input())

product = 1
for u in range(num):
    product *= (u + 1)
print(f"Q2: {num}! = {product}\n")

#Question 3:

dict3 = {}

num2 = int(input())

for o in range(1, num2 + 1):
    dict3[o] = o * o

print(f"Q3: {dict3}\n")

#Question 4:

nums2 = input()
list5 = nums2.split(",")

print(f"Q4: {list5}")
print(f"    {tuple(list5)}\n")

#Question 5:

class StringInOut:
    def __init__(self):
        self.HeldString = ""

    def getString(self):
        self.HeldString = input()

    def printString(self):
        print(self.HeldString)

sio = StringInOut()
sio.getString()

print("Q5: ", end = "") # Just for terminal readability

sio.printString()