def calculate(expression):
    """
    Evaluate a math expression and return the result.
    """
    try:
        result = eval(expression)
        return result
    except Exception as e:
        raise ValueError(f"Invalid expression: {str(e)}")

def main():
    """
    Run the calculator in interactive mode.
    """
    while True:
        user_input = input("Enter a math problem (or 'quit' to exit): ")
        if user_input.lower() == 'quit':
            break
        try:
            result = calculate(user_input)
            print("Result:", result)
        except ValueError as e:
            print("Error:", str(e))

if __name__ == "__main__":
    main()