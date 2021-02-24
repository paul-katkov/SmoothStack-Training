#1:

import numpy as np

#2:

print(f"2: {np.zeros(10)}\n")

#3:

print(f"3: {np.ones(10)}\n")

#4:

print(f"4: {np.ones(10) * 5}\n")

#5:

print(f"5: {np.arange(10, 51)}\n")

#6:

print(f"6: {np.arange(10, 51, 2)}\n")

#7:

print("7:")
print(np.arange(0, 9).reshape(3, 3))
print("")

#8:

print("8:")
print(np.eye(3))
print("")

#9:

print(f"9: {np.random.randint(0, 2)}")