import os
import requests
import zipfile
import shutil
import filecmp

# Define the paths
root_dir = "pengsystems"
updater_dir = os.path.join(root_dir, "updater")
new_dir = os.path.join(updater_dir, "new")

# Download the zip file
def download_zip(url, filename):
    """Download a zip file from a URL and save it to a file."""
    response = requests.get(url)
    with open(os.path.join(updater_dir, filename), 'wb') as f:
        f.write(response.content)

# Unpack the zip file
def unpack_zip(filename):
    """Unpack a zip file to a directory."""
    with zipfile.ZipFile(os.path.join(updater_dir, filename), 'r') as zip_ref:
        zip_ref.extractall(new_dir)

# Compare directories and update files
def update_files(src_dir, dst_dir):
    """Compare two directories and update files in the destination directory."""
    for root, dirs, files in os.walk(src_dir):
        for dir in dirs:
            src_path = os.path.join(root, dir)
            dst_path = os.path.join(dst_dir, os.path.relpath(src_path, src_dir))
            if not os.path.exists(dst_path):
                os.makedirs(dst_path)
        for file in files:
            src_path = os.path.join(root, file)
            dst_path = os.path.join(dst_dir, os.path.relpath(src_path, src_dir))
            if dst_path == os.path.join(root_dir, "user_data", "login_data.txt"):
                continue  # Skip updating the login_data.txt file
            if not os.path.exists(dst_path) or not filecmp.cmp(src_path, dst_path):
                if not os.path.exists(os.path.dirname(dst_path)):
                    os.makedirs(os.path.dirname(dst_path))
                shutil.copy2(src_path, dst_path)
    # Update the penguin-systems.py file
    penguin_systems_src = os.path.join(src_dir, "penguin-systems.py")
    penguin_systems_dst = os.path.join(dst_dir, "penguin-systems.py")
    if os.path.exists(penguin_systems_src) and (not os.path.exists(penguin_systems_dst) or not filecmp.cmp(penguin_systems_src, penguin_systems_dst)):
        shutil.copy2(penguin_systems_src, penguin_systems_dst)
        
# Main function
def main():
    url = "www.sky-network,org/pengsystems.zip"  # Replace with the actual URL
    filename = "pengsystems.zip"
    
    # Create the updater directory if it doesn't exist
    if not os.path.exists(updater_dir):
        os.makedirs(updater_dir)
    
    # Download the zip file
    download_zip(url, filename)
    
    # Unpack the zip file
    unpack_zip(filename)
    
    # Update files
    update_files(new_dir, root_dir)
    
    # Remove the new directory
    shutil.rmtree(new_dir)
    
    # Remove the zip file
    os.remove(os.path.join(updater_dir, filename))

if __name__ == "__main__":
    main()