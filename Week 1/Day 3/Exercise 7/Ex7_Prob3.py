import random

num = random.randint(1, 9)

print("Guess a number between 1 and 9:", end = " ")

guess = int(input())

while guess != num:
    print("Not quite. Try again:", end = " ")
    guess = int(input())
else:
    print("Well guessed!")
