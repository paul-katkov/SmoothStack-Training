#4:

print("4:")

for i in range(-4, 5):
    star = "*" * (5 - abs(i))
    print(star)

print("")

#6:

print("6: Please input a word:", end = " ")
print(f"{input()[::-1]}\n")

#7:

print("7:", end = " ")

def EvenAndOdd(nums):
    even = 0
    odd = 0

    for num in nums:
        if num % 2 == 0:
            even += 1
        else:
            odd += 1
    
    print(f"Number of even numbers: {even}")
    print(f"Number of odd numbers: {odd}\n")

numbers = (1, 2, 3, 4, 5, 6, 7, 8, 9)

EvenAndOdd(numbers)

#8:

print("8:", end = " ")

def ListItemType(lst):
    typelist = []

    for item in lst:
        typelist += [type(item)]

    print(f"{typelist}\n")

datalist = [1452, 11.23, 1 + 2j, True, 'w3resource', (0, -1), [5, 12], {"class":'V', "section":'A'}]

ListItemType(datalist)

#9:

print("9:", end = " ")

for i in range(7):
    if i == 3 or i == 6:
        continue
    else:
        print(i, end = " ")

print("\n")