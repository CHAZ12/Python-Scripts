

Code = "VqkmRwjaw}[wt~mlQ|)"
for d in range(-10,10):
    decript = ""
    distance = d
    for i in Code:
        Cipher = ord(i) + distance
        decript += chr(Cipher)
    print(decript + "\n")
    