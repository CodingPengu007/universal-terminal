import os
import sys
import getpass
import bcrypt

# Ensure the parent directory of 'universal_systems' is in the system path
sys.path.insert(0, os.path.dirname(__file__))

from universal_systems.programs.calculator import calc
from universal_systems.system_programs.login_system import *

def get_current_username(username):
    # Return the current username
    return username

def control_center():
    commands = {
        "calc": calc, 
        "help": lambda: print("Available commands: calc, help, exit, logout, signup, usr -list"),
        "exit": lambda: sys.exit(0),
        "logout": lambda: None,
        "signup": lambda: None
    }

    username = login()

    while True:
        user_input = input("Enter a command: ")
        parts = user_input.split()

        if username is None:
            if parts[0] == "signup":
                signup()
                username = login()
            elif parts[0] == "login":
                username = login()
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
                        if command in commands:
                            if command == "calc":
                                expression = " ".join(parts[2:])
                                result = calc(expression)
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
        elif parts[0] == "usr" and parts[1] == "-list":
            user_list = get_user_list()
            for user in user_list:
                print(user)
        elif parts[0] in commands:
            if parts[0] == "calc":
                expression = " ".join(parts[1:])
                result = calc(expression)
                print(f"The result of {expression} is {result}")
            else:
                commands[parts[0]]()
        else:
            print("Unknown command. Type 'help' for available commands.")

if __name__ == "__main__":
    from universal_systems.system_programs.login_system import login, is_admin, signup, encrypt_password, user_data_folder, get_user_list
    control_center()