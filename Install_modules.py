import os
import shutil
import re
import subprocess
import sys

# Lista modułów do sprawdzenia i ewentualnej instalacji
modules = [
    ('tqdm', 'tqdm'),
    ('zipfile', None),  # zipfile jest częścią standardowej biblioteki
    ('rarfile', 'rarfile')
    ('art', 'art')
]

# Funkcja do sprawdzania i instalacji modułu
def check_and_install(module_name, package_name=None):
    try:
        __import__(module_name)
        print(f"Moduł {module_name} jest już zainstalowany.")
    except ImportError:
        if package_name is None:
            package_name = module_name
        print(f"Instalowanie modułu {module_name}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"Moduł {module_name} został zainstalowany.")

# Sprawdzenie i instalacja modułów
for module_name, package_name in modules:
    check_and_install(module_name, package_name)

# Importowanie sprawdzonych modułów
from tqdm import tqdm
import zipfile
import rarfile

print("\nWszystkie wymagane moduły są zainstalowane.\n")
input("Wciśnij ENTER by zakończyć: ")