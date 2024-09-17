import os
import sys
import getpass
import hashlib

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'programs'))

from pengsystems.programs.calculator import calculate
from pengsystems.system_programs.login_system import login_system, is_admin, signup, encrypt_password, user_data_folder

def get_current_username(username):
    # Return the current username
    return username

def control_center():
    commands = {
        "calc": calculate,
        "help": lambda: print("Available commands: calc, help, exit, logout, signup"),
        "exit": lambda: sys.exit(0),
        "logout": lambda: None,
        "signup": lambda: None
    }

    username = login_system()

    while True:
        user_input = input("Enter a command: ")
        parts = user_input.split()

        if username is None:
            if parts[0] == "signup":
                signup()
                username = login_system()
            elif parts[0] == "login":
                username = login_system()
            else:
                print("You are not logged in. Please login or signup first.")
                continue

        if parts[0] == "sudo":
            if not is_admin(get_current_username(username)):
                print("You are not authorized to use sudo commands.")
                continue

            password = getpass.getpass("Enter your password again to verify your identity: ")
            encrypted_password = encrypt_password(password)

            with open(os.path.join(user_data_folder, 'user-data.txt'), 'r') as file:
                for line in file:
                    stored_username, stored_password = line.strip().split(':')
                    if stored_username == get_current_username(username) and stored_password == encrypted_password:
                        # Password is correct, proceed with the sudo command
                        command = " ".join(parts[1:])
                        if command == "apt-get update":
                            import pengsystems.updater.updater as updater
                            updater.update()
                            print("Update successful!")
                        elif command in commands:
                            if command == "calc":
                                expression = " ".join(parts[2:])
                                result = calculate(expression)
                                print(f"The result of {expression} is {result}")
                            else:
                                commands[command]()
                        else:
                            print("Unknown command. Type 'help' for available commands.")
                        break
                else:
                    print("Invalid password. Access denied.")
        elif parts[0] == "logout":
            print("You have been logged out.")
            username = None
        elif parts[0] == "signup":
            print("You need to logout before signing up a new user.")
        elif parts[0] in commands:
            if parts[0] == "calc":
                expression = " ".join(parts[1:])
                result = calculate(expression)
                print(f"The result of {expression} is {result}")
            else:
                commands[parts[0]]()
        else:
            print("Unknown command. Type 'help' for available commands.")

if __name__ == "__main__":
    control_center()