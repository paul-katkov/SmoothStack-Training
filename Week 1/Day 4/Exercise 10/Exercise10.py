def BMI(weight, height):
    if(weight / height**2 < 18.5):
        return "under"
    elif(weight / height**2 < 25.0):
        return "normal"
    elif(weight / height**2 < 30.0):
        return "over"
    else:
        return "obese"

num = int(input())
BMIs = []

for i in range(num):
    h, w = input().split()
    h, w = [float(h), float(w)]
    BMIs += [BMI(h, w)]

print(BMIs)
