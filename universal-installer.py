import os
import pathlib
import shutil

def get_desktop_path():
    """Get the path to the desktop folder."""
    if os.name == 'nt':  # Windows
        desktop_path = pathlib.Path(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'))
    else:  # Linux
        desktop_path = pathlib.Path(os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop'))
        if not desktop_path.exists():
            # Try to find the desktop folder in the user's home directory
            for folder in os.listdir(os.path.expanduser('~')):
                if folder.lower() in ['desktop', 'schreibtisch', 'bureau', 'escritorio', 'desktop']:
                    desktop_path = pathlib.Path(os.path.join(os.path.expanduser('~'), folder))
                    break
    return desktop_path

def get_downloads_path():
    """Get the path to the downloads folder."""
    if os.name == 'nt':  # Windows
        downloads_path = pathlib.Path(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Downloads'))
    else:  # Linux
        downloads_path = pathlib.Path(os.path.join(os.path.join(os.path.expanduser('~')), 'Downloads'))
    return downloads_path

def move_file():
    """Move the file 'universal-terminal.zip' from the downloads folder to the desktop folder."""
    downloads_path = get_downloads_path()
    desktop_path = get_desktop_path()
    
    file_path = downloads_path / 'universal-terminal.zip'
    if file_path.exists():
        try:
            dest_file_path = desktop_path / file_path.name
            if dest_file_path.exists():
                print(f"File '{file_path.name}' already exists in '{desktop_path}'. Overwrite? (y/n)")
                response = input()
                if response.lower() == 'y':
                    shutil.move(str(file_path), str(desktop_path))
                    print(f"Moved '{file_path.name}' to '{desktop_path}'")
                    delete_self()
                else:
                    print(f"File '{file_path.name}' not moved.")
            else:
                shutil.move(str(file_path), str(desktop_path))
                print(f"Moved '{file_path.name}' to '{desktop_path}'")
                delete_self()
        except Exception as e:
            print(f"Failed to move '{file_path.name}': {str(e)}")
    else:
        print(f"'{file_path.name}' not found in '{downloads_path}'")

def delete_self():
    """Delete the script file."""
    script_path = pathlib.Path(__file__)
    try:
        os.remove(str(script_path))
        print(f"Deleted script file '{script_path.name}'")
    except Exception as e:
        print(f"Failed to delete script file: {str(e)}")

if __name__ == "__main__":
    move_file()
