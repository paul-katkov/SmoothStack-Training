#1:

print("1:", end = " ")

def func():
    print("Hello World")

func()

print("")

#2:

print("2:", end = " ")

def func2(name):
    print(f"Hi, my name is {name}\n")

func2("Google")

#3:

print("3:", end = " ")

def func3(x, y, z):
    if z:
        return x
    else:
        return y

print(f"{func3('hello', 'goodbye', False)}\n")

#4:

print("4: (using 3 and 5 as an example)", end = " ")

def func4(x, y):
    return x * y

print(f"{func4(3, 5)}\n")

#5:

print("5: (using 86 as an example)", end = " ")

def is_even(num):
    return (num % 2 == 0)

print(f"{is_even(86)}\n")

#6:

print("6: (using 7 and 7 as an example)", end = " ")

def func6(a, b):
    return (a > b)

print(f"{func6(7, 7)}\n")

#7:

print("7: (using 0, 2, 1, 8, 2, 0, 2, 1 as an example)", end = " ")

def func7(*nums):
    sum = 0
    for num in nums:
        sum += num
    return sum

print(f"{func7(0, 2, 1, 8, 2, 0, 2, 1)}\n")

#8:

print("8: (using 1, 2, 3, 4, 5, 6, 7, 8, 9 as an example)", end = " ")

def func8(*nums):
    evens = [num for num in nums if num % 2 == 0]
    return evens

print(f"{func8(1, 2, 3, 4, 5, 6, 7, 8, 9)}\n")

#9:

print("9: (using 'SmoothStack' as an example)", end = " ")

def func9(s):
    output = ""
    for i in range(len(s)):
        if i % 2 == 0:
            output += s[i].upper()
        else:
            output += s[i].lower()
    return output

print(func9("SmoothStack") + "\n")

#10:

print("10:", end = " ")

def func10(a, b):
    if a % 2 != 0 or b % 2 != 0:
        return max(a, b)
    else:
        return min(a, b)

print(f"(using 8 and 9 as input) {func10(8, 9)}")
print(f"    (using 8 and 6 as input) {func10(8, 6)}\n")

#11:

print("11:", end = " ")

def func11(word1, word2):
    return (word1.lower()[0] == word2.lower()[0])

print(f"(using 'SmoothStack' and 'smoothstack' as inputs) {func11('SmoothStack', 'smoothstack')}")
print(f"    (using 'apple' and 'banana' as inputs) {func11('apple', 'banana')}\n")

#12:

print("12: (using 10 as an example)", end = " ")

def func12(num):
    return (7 + 2 * (7 - num))

print(f"{func12(10)}\n")

#13:

print("13: (using 'apple' as an example)", end = " ")

def func13(s):
    output = ""
    for i in range(len(s)):
        if i == 0 or i == 3:
            output += s[i].upper()
        else:
            output += s[i]
    return output

print(func13("apple"))