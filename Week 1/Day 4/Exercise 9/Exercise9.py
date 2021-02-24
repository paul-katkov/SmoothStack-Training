#1:

l1 = [[34587, "Learning Python, Mark Lutz", 4, 40.95], [98762, "Programming Python, Mark Lutz", 5, 56.80], [77226, "Head First Python, Paul Barry", 3, 32.95], [88112, "Einführung in Python3, Bernd Klein", 3, 24.99]]

#2:

print("2:", end = " ")

is_enough = lambda row : (row[0], round(row[2] * row[3], 2)) if row[2] * row[3] >= 100 else (row[0], round(row[2] * (row[3] + 10), 2))

l1_new = list(map(is_enough, l1))

print(l1_new)

#3:

print("3:", end = " ")

l2 = [34587, ("LP, ML", 4, 40.95), 98762, ("PP, ML", 5, 56.80), 77226, ("HFP, PB", 3, 32.95), 88112, ("EiP3, BK", 3, 24.99)]

is_enough2 = lambda entry : (entry, round(l2[l2.index(entry) + 1][1] * l2[l2.index(entry) + 1][2], 2)) if l2.index(entry) % 2 == 0 and l2[l2.index(entry) + 1][1] * l2[l2.index(entry) + 1][2] >= 100 else ((entry, round(l2[l2.index(entry) + 1][1] * (l2[l2.index(entry) + 1][2] + 10), 2)) if l2.index(entry) % 2 == 0 else None)

l2_new = [i for i in list(map(is_enough2, l2)) if i != None]

print(l2_new)
