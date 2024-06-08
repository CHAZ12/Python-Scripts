import time

start = 0
print(" This program will solve linear a interpolation with y2 as unknown")
while start == 0:
    # first variables
    x1 = float(input("Enter x1 as integer: "))
    x2 = float(input("Enter x2 as integer: "))
    x3 = float(input("Enter x3 as integer: "))

    y1 = float(input("Enter y1 as integer: "))
    y3 = float(input("Enter y3 as integer: "))

    x = (((x2 - x1) / (x3 - x1)) * (y3 - y1) + y1)

    print(str(x) + ' is the value for x')
    UserInput = (input("You would like to restart program? (y/n)"))
    if UserInput == 'y':
        start = 0
    else:
        print('Program us closing')
        time.sleep(2)
        start = 1