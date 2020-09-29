import random

n = random.randrange(10)
for x in range(3):
    guess = int(input("Enter your guess: "))
    if guess == n:
        break

if guess == n:
    print("You win!")
else:
    print("You lose!")