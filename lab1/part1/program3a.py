n = int(input("How many Fibonacci numbers would you like to generate? "))
fs = []
while n > 0:
    if fs == [] or len(fs) == 1:
        fs.append(1)
    else:
        fs.append(fs[-1] + fs[-2])
    n -= 1
    
print("The Fibonacci Sequence is: " + str(fs))