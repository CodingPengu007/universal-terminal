import os
import getpass
import hashlib

user_data_folder = os.path.join(os.path.dirname(__file__), '..', '..', 'user-data')
admin_list_file = os.path.join(user_data_folder, 'admin_list.txt')
user_data_file = os.path.join(user_data_folder, 'user-data.txt')

def encrypt_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def signup():
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    confirm_password = getpass.getpass("Confirm your password: ")

    if password != confirm_password:
        print("Passwords do not match. Please try again.")
        return False

    with open(user_data_file, 'a') as file:
        file.write(f"{username}:{encrypt_password(password)}\n")

    if not os.path.exists(admin_list_file) or os.path.getsize(admin_list_file) == 0:
        with open(admin_list_file, 'w') as file:
            file.write(username + "\n")
        print("You are the first user, you have been added as an admin.")
    else:
        print("Signup successful!")

    return username

def login():
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")

    with open(user_data_file, 'r') as file:
        for line in file:
            stored_username, stored_password = line.strip().split(':')
            if stored_username == username and stored_password == encrypt_password(password):
                print("Login successful!")
                return username

    print("Invalid username or password.")
    return None

def is_admin(username):
    with open(admin_list_file, 'r') as file:
        return username in [line.strip() for line in file]

def login_system():
    while True:
        user_input = input("Enter 'login' to login or 'signup' to signup: ")
        if user_input == "login":
            username = login()
            if username:
                break
        elif user_input == "signup":
            username = signup()
            break
        else:
            print("Invalid command. Type 'login' or 'signup' to proceed.")

    print("You have been logged in successfully!")

    if is_admin(username):
        print("You are an admin!")

    while True:
        user_input = input("Enter 'logout' to logout: ")
        if user_input == "logout":
            print("You have been logged out. Please login or signup to access the system again.")
            login_system()
            break
        else:
            print("Invalid command. Type 'logout' to proceed.")

login_system()