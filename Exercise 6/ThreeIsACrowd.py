def crowd_test(crowd):
    if len(crowd) > 2:
        print("The room is crowded.")

names = ["Leo", "Don", "Mike", "Raf"]

crowd_test(names)

while(len(names) > 2):
    names.pop()

crowd_test(names)