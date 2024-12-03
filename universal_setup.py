import os
import sys
import subprocess
import platform
import zipfile
import shutil

def create_directories():
    """Create the universal_systems directory structure."""
    base_dir = os.getcwd()
    universal_systems_dir = os.path.join(base_dir, "universal_systems")
    user_data_dir = os.path.join(universal_systems_dir, "user_data")
    programs_dir = os.path.join(universal_systems_dir, "programs")
    system_programs_dir = os.path.join(universal_systems_dir, "system_programs")
    
    # Create the main directory
    os.makedirs(user_data_dir, exist_ok=True)
    os.makedirs(programs_dir, exist_ok=True)
    os.makedirs(system_programs_dir, exist_ok=True)

    # Create user_data files
    user_data_file = os.path.join(user_data_dir, "user_data.txt")
    if not os.path.exists(user_data_file):
        with open(user_data_file, 'w') as f:
            f.write("User  data goes here.\n")  # You can customize this content as needed

    with open(os.path.join(user_data_dir, "login_data.txt"), 'w') as f:
        f.write("Login data goes here.\n")
    with open(os.path.join(user_data_dir, "admin_list.txt"), 'w') as f:
        f.write("Admin list goes here.\n")
    with open(os.path.join(user_data_dir, "user_list.txt"), 'w') as f:
        f.write("User  list goes here.\n")

    print("Directory structure created successfully.")

def move_and_unpack_zip(zip_filename, target_dir):
    """Move a zip file to the target directory and unpack it."""
    base_dir = os.getcwd()
    zip_path = os.path.join(base_dir, zip_filename)
    
    if not os.path.exists(zip_path):
        print(f"Error: {zip_filename} does not exist in the current directory.")
        return

    # Move the zip file
    shutil.move(zip_path, target_dir)
    print(f"Moved {zip_filename} to {target_dir}")

    # Unpack the zip file
    with zipfile.ZipFile(os.path.join(target_dir, zip_filename), 'r') as zip_ref:
        zip_ref.extractall(target_dir)
    print(f"Unpacked {zip_filename} in {target_dir}")

    # Delete the zip file after unpacking
    os.remove(os.path.join(target_dir, zip_filename))
    print(f"Deleted {zip_filename} after unpacking.")

def create_virtualenv(env_name):
    """Create a virtual environment."""
    try:
        subprocess.check_call([sys.executable, '-m', 'venv', env_name])
        print(f"Virtual environment '{env_name}' created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error creating virtual environment: {e}")
        print("Make sure you have Python installed and the 'venv' module available.")
        sys.exit(1)

def activate_virtualenv(env_name):
    """Activate the virtual environment."""
    if platform.system() == "Windows":
        activate_script = os.path.join(env_name, 'Scripts', 'activate')
    else:
        activate_script = os.path.join(env_name, 'bin', 'activate')

    return activate_script

def install_bcrypt(env_name):
    """Install bcrypt in the virtual environment."""
    if platform.system() == "Windows":
        pip_executable = os.path.join(env_name, 'Scripts', 'pip')
    else:
        pip_executable = os.path.join(env_name, 'bin', 'pip')

    try:
        subprocess.check_call([pip_executable, 'install', 'bcrypt'])
        print("bcrypt installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing bcrypt: {e}")
        print("Please check your internet connection or try installing manually.")
        sys.exit(1)

def main():
    env_name = "universal_systems_venv"  # Name of the virtual environment

    # Create directory structure
    create_directories()

    # Move and unpack zip files
    move_and_unpack_zip("programs.zip", os.path.join(os.getcwd(), "universal_systems", "programs"))
    move_and_unpack_zip("system_programs.zip", os.path.join(os.getcwd(), "universal_systems", "system_programs"))
    
    # Move and unpack universal_systems.zip
    move_and_unpack_zip("universal_systems.zip", os.path.join(os.getcwd(), "universal_systems"))

    # Create a virtual environment
    create_virtualenv(env_name)

    # Activate the virtual environment
    activate_command = activate_virtualenv(env_name)
    print(f"To activate the virtual environment, run the following command in your terminal:")
    print(f"source {activate_command}" if platform.system() != "Windows" else f"{activate_command}")

    # Install bcrypt
    install_bcrypt(env_name)

if __name__ == "__main__":
    main()