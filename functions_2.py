
def numbers():
    try:
        user = int(input("Enter a number: "))
        if user ==  0:
            message = "The number is zero"
        elif user < 0:
            message = "The number is negative"
        elif user < 0 and user  % 2 == 0:
            message = "The number is positive and even"
        elif user < 0 and  user % 2 != 0:
            message = "The number is negative and odd"
        elif user > 0 and user % 2 == 0:
            message = "The number is positive and even"

        else:
            message = "The number is positive and odd"
        return message
    except ValueError:
        return "Invalid Input"
    
print(numbers())
