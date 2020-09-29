print("Welcome to the birthday dictionary. We know the birthdays of:")
birthdays = {"Albert Einstein": "03/14/1879", "Benjamin Franklin": "01/17/1706", "Ada Lovelace": "12/10/1815"}
for person in birthdays:
    print(person)
name = input("Who's birthday do you want to look up? ")
if(name in birthdays):
    print(name + "'s birthday is " + birthdays[name] + ".")
else:
    print("Sorry, couldn't find that name")