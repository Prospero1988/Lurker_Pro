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
    #print(f"Searching in: {default_dir}")  # Debug: wyświetl ścieżkę katalogu
    #print(f"Using pattern: {pattern}")     # Debug: wyświetl używany wzorzec
    for root, dirs, files in os.walk(default_dir):
        #print(f"Checking directory: {root}")  # Debug: wyświetl przeszukiwany katalog
        for file in files:
            progress_bar.update(1)
            file_path = os.path.join(root, file)
            #print(f"Checking file: {file_path}")  # Debug: wyświetl przeszukiwany plik
            if pattern.search(file):
                #print(f"Match found: {file_path}")  # Debug: wyświetl znaleziony plik
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

def hello():
    """Displays a welcome screen."""
    info = """
A script for recursively searching a specified folder
(default is NMR spectrum disk) to find specific files.
Search based on a list of keywords (or filenames).
The script also searches the contents of RAR and ZIP archives.
    """
    # Clear the console and display the ASCII art logo
    subprocess.call('cls' if os.name == 'nt' else 'clear', shell=True)
    print('')
    ascii_art= text2art("LURKER PRO v3")
    print('')

hello()

# Folder management
default_dir = r'\\data02.celon.local\NMR'
try:
    check_dir = input(f"\nDo you want to search the default NMR disk folder?\nChoose [n] to specify a different path.\n\n{default_dir} [y/n]: ").strip().lower()
except Exception as e:
    print(f"An error occurred while trying to read the path: {e}")
    exit()

while True:
    if check_dir == 'y':
        while True:
            if not os.path.exists(default_dir):
                print("The default folder does not exist. You must manually define a folder to search.")
                default_dir = get_directory_from_user()
            else:
                print(f"\nThe folder to be searched will be: {default_dir}")
                break
        break
    elif check_dir == 'n':
        default_dir = get_directory_from_user()
        print(f"The folder to be searched will be: {default_dir}")
        break
    else:
        check_dir = input("Choose only [y/n]: ").strip().lower()

# Creating a folder where the found files will be saved.
output_dir = 'output'
output_path = os.path.join(os.getcwd(), output_dir)
os.makedirs(output_path, exist_ok=True)
print(f"The found files will be saved to the folder: {os.path.abspath(output_path)}")

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
