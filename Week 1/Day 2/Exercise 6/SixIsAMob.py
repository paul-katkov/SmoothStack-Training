def crowd_test(crowd):
    if len(crowd) > 5:
        print("There is a mob in the room.")
    elif len(crowd) > 2:
        print("The room is crowded.")
    elif len(crowd) > 0:
        print("The room is not very crowded.")
    else:
        print("The room is empty.")

names = ["Leo", "Don", "Mike", "Raf", "Splinter", "April"]

crowd_test(names)

while(len(names) > 5):
    names.pop()

crowd_test(names)

while(len(names) > 2):
    names.pop()

crowd_test(names)

while(len(names) > 0):
    names.pop()

crowd_test(names)
