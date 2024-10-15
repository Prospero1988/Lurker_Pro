try:
    import os
    import shutil
    import re
    from tqdm import tqdm
    import zipfile
    import rarfile
    import subprocess
    from art import text2art
    
except ImportError as e:
    print(f"Error importing module: {e}")
    input("Press Enter to exit.")
    exit()

def get_directory_from_user():
    """Prompts the user to enter a directory path and validates it."""
    while True:
        try:
            dir_path = input("Enter the full path to the folder to be searched: ").strip()
            if not dir_path:
                print("The path cannot be empty.")
                continue
            if not os.path.exists(dir_path):
                print("The folder does not exist.")
            else:
                return dir_path
        except Exception as e:
            print(f"Error: {e}")

def search_folders(default_dir, pattern, output_path, progress_bar):
    # print(f"Searching in: {default_dir}")  # Debug: display the directory path
    # print(f"Using pattern: {pattern}")     # Debug: display the pattern being used
    for root, dirs, files in os.walk(default_dir):
        # print(f"Checking directory: {root}")  # Debug: display the directory being searched
        for file in files:
            progress_bar.update(1)
            file_path = os.path.join(root, file)
            # print(f"Checking file: {file_path}")  # Debug: display the file being searched
            if pattern.search(file):
                # print(f"Match found: {file_path}")  # Debug: display the found file
                destination_path = os.path.join(output_path, os.path.basename(file_path))
                if not os.path.exists(destination_path):
                    try:
                        shutil.copy(file_path, destination_path)
                        print(f"Copied: {file_path} -> {destination_path}")
                    except Exception as e:
                        print(f"Error copying file: {file_path} -> {destination_path}: {e}")

        for file in files:
            progress_bar.update(1)
            file_name = os.path.basename(file)
            if file_name.endswith('.zip'):
                archive_path = os.path.join(root, file)
                with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                    for name in zip_ref.namelist():
                        if name.endswith('/'):
                            continue  # skip folders inside the archive
                        source_folder = os.path.split(name)[-2]
                        if pattern.search(source_folder):
                            try:
                                destination_path = os.path.join(output_path, os.path.basename(source_folder))
                                if not os.path.exists(destination_path):
                                    os.makedirs(destination_path)
                                zip_ref.extract(name, destination_path)
                            except Exception as e:
                                print(f"Error while extracting ZIP archive file {source_folder}: {e}")
                            print(f"Found and copied folder: {source_folder} -> {destination_path}: Archive file in: {archive_path}")

            elif file_name.endswith('.rar'):
                archive_path = os.path.join(root, file)
                with rarfile.RarFile(archive_path, 'r') as rar_ref:
                    for name in rar_ref.namelist():
                        if name.endswith('/'):
                            continue  # skip folders inside the archive
                        source_folder = os.path.split(name)[-2]
                        if pattern.search(source_folder):
                            try:
                                destination_path = os.path.join(output_path, os.path.basename(source_folder))
                                if not os.path.exists(destination_path):
                                    os.makedirs(destination_path)
                                rar_ref.extract(name, destination_path)
                            except Exception as e:
                                print(f"Error while extracting RAR archive file {source_folder}: {e}")
                            print(f"Found and copied folder: {source_folder} -> {destination_path}: Archive file in: {archive_path}")


    
"""
A script for recursively searching a specified folder
(default is NMR spectrum disk) to find specific files.
Search based on a list of keywords (or filenames).
The script also searches the contents of RAR and ZIP archives.
"""
    
"""Displays a welcome screen."""
# Clear the console and display the ASCII art logo
subprocess.call('cls' if os.name == 'nt' else 'clear', shell=True)
print('')
ascii_art = text2art("LURKER+PRO")
print(ascii_art)
print('')

# ANSI color
COLORS = ['\033[38;5;46m',    # Green
          '\033[38;5;196m',   # Red
          '\033[38;5;214m'    # Orange
         ]
RESET = '\033[0m'

# Folder management
default_dir = os.getcwd()
try:
    check_dir = input(f"\nThe search will be performed in the default folder: {COLORS[2]}{default_dir}{RESET}\n"
                      f"Choose {COLORS[0]}[y]{RESET} to specify a different path or {COLORS[1]}[n]{RESET} to"
                      f" proceed in default folder.\n\n"
                      f"Do you want to specify a folder to search? [{COLORS[0]}[y]{RESET}/{COLORS[1]}[n]{RESET}]: ").strip().lower()
except Exception as e:
    print(f"An error occurred while trying to read the path: {e}")
    exit()

while True:
    if check_dir == 'n':
        while True:
            if not os.path.exists(default_dir):
                print(f"{COLORS[1]}The default folder does not exist. You must manually define a folder to search.{RESET}")
                default_dir = get_directory_from_user()
            else:
                print(f"\nThe folder to be searched will be: {COLORS[2]}{default_dir}{RESET}")
                break
        break
    elif check_dir == 'y':
        default_dir = get_directory_from_user()
        print(f"The folder to be searched will be: {COLORS[2]}{default_dir}{RESET}")
        break
    else:
        check_dir = input(f"\n{COLORS[1]}Choose only [y/n]: {RESET}").strip().lower()

# Creating a folder where the found files will be saved.
output_dir = 'output'
output_path = os.path.join(os.getcwd(), output_dir)
os.makedirs(output_path, exist_ok=True)
print(f"The found files will be saved to the folder: {COLORS[2]}{os.path.abspath(output_path)}{RESET}")

# File search module
phrases_input = input("\nEnter the name of the file, files, or keywords. \nSeparate them by commas: ")
print()
phrases = [phrase.strip() for phrase in phrases_input.replace(", ", ",").split(",")]

# Creating a regex pattern that matches any of the phrases
pattern = re.compile('|'.join(map(re.escape, phrases)), re.IGNORECASE)

# Creating only one instance of tqdm
with tqdm(desc="Searching files", unit=" file", position=0) as progress_bar:
    search_folders(default_dir, pattern, output_path, progress_bar)

print(f"\n======================")
input("Press Enter to finish. \n")
