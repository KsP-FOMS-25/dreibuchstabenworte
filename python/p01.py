secretnumber = 12344;
inputnumber = 0
count = 0

while inputnumber != secretnumber:
    inputnumber = int(input("inputnumber Number: "))
    if inputnumber < secretnumber:
        print("Number smaller than secret number")
    if inputnumber > secretnumber:
        print("Number bigger than secret number")
    count = count + 1
print("Success after {0} tries".format(count))