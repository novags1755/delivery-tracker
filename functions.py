def categorize_age():
    try:
        x = int(input("Enter Your Age:"))
        if x < 0:
            message = "Invalid Input"
            return message
        else:
            if x < 13:
                message = "You are a kid"
            elif x < 20:
                message = "You are a teenager"
            elif x < 65:
             message = "You are an adult"
            else:
                message = "You are an elder" 
            return message
    except ValueError:
        return "Invalid Input"

print(categorize_age())