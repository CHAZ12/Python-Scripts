a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
b = [[0 for y in range(3)]
     for x in range(3)]
count = 0
i = 0
f = 2
g = 0
int = len(a)
loop = True
while loop:
    if count < int:
        for x in a[f]:
            b[i][g] = x
            i += 1
            count += 1
    else:
        count = 0
        f = f-1
        g = g + 1
        i = 0
        if f < 0:
            loop = False
            print(b)