import winreg
import argparse
import os
import re

def find_guids_in_cs_files(directory, search_text):
    guid_pattern = re.compile(r'Guid\("([A-Fa-f0-9-]+)"\)')
    guids = []

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.cs'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            if search_text in line:
                                match = guid_pattern.search(line)
                                if match:
                                    guids.append(match.group(1))
                except Exception as e:
                    print(f"Errore durante la lettura del file {file_path}: {e}")

    return guids

def read_registry_value(key_path):
    try:
        # Apri la chiave del registro
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
            values = {}
            i = 0
            while True:
                try:
                    value_name, value_data, _ = winreg.EnumValue(key, i)
                    values[value_name] = value_data
                    i += 1
                except OSError:
                    break
            return values
    except FileNotFoundError:
        print(f"Chiave non trovata: {key_path}")
    except PermissionError:
        print(f"Permessi insufficienti per accedere a: {key_path}")
    except Exception as e:
        print(f"Errore durante l'accesso a {key_path}: {e}")

    return None

def check_registry_for_guids(guids):
    base_paths = [
        r"SOFTWARE\Classes\CLSID\{guid}\InprocServer32\1.6.6.3",
        r"SOFTWARE\Classes\ILFashion.CILFashion\CLSID",
        r"SOFTWARE\Classes\WOW6432Node\CLSID\{guid}\InprocServer32\1.6.6.3",
        r"SOFTWARE\WOW6432Node\Classes\CLSID\{guid}\InprocServer32\1.6.6.3",
    ]

    for guid in guids:
        print(f"\nVerifica del GUID: {guid}")
        for path in base_paths:
            formatted_path = path.replace("{guid}", guid)
            values = read_registry_value(formatted_path)
            if values:
                print(f"Valori trovati in {formatted_path}: {values}")
            else:
                print(f"Nessun valore trovato o impossibile leggere {formatted_path}")

def main():
    parser = argparse.ArgumentParser(description="Trova GUID nei file .cs e verifica le chiavi di registro.")
    parser.add_argument("directory", type=str, help="Percorso iniziale della directory da scansionare")
    args = parser.parse_args()

    search_text = '[ComVisible(true), ClassInterface(ClassInterfaceType.None), Guid('
    guids_found = find_guids_in_cs_files(args.directory, search_text)

    if not guids_found:
        print("Nessun GUID trovato.")
    else:
        print(f"Trovati GUID: {guids_found}")
        check_registry_for_guids(guids_found)

if __name__ == "__main__":
    main()