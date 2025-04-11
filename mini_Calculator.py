def calculate():
    num1 = float(input("Enter first number: "))
    operator = input("Enter operator (+, -, *, /): ")
    num2 = float(input("Enter second number: "))

    if operator == "+":
        result = num1 + num2
    elif operator == "-":
        result = num1 - num2
    elif operator == "*":
        result = num1 * num2
    elif operator == "/":
        if num2 == 0:
            result = "Error: Cannot divide by zero"
        else:
            result = num1 / num2
    else:
        result = "Invalid operator"

    print("The result is:", result)


# Loop that keeps calculator running
while True:
    user_input = input("Type 'yes' to calculate or 'done' to exit: ").lower()
    if user_input == "done":
        print("Calculator closed. Goodbye!")
        break
    elif user_input == "yes":
        calculate()
    else:
        print("Please type 'yes' or 'done'")
