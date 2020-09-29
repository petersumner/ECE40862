a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
print(a)
n = int(input("Enter number: "))
new = []
for x in a:
    if x < n:
        new.append(x)
print("The new list is " + str(new))