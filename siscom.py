import winreg
import argparse
import os
import re
from rich import print

def read_registry_recursive(key_path, base_hive=winreg.HKEY_LOCAL_MACHINE):
    """Legge ricorsivamente tutti i dati e le sottochiavi dal percorso del registro specificato."""
    try:
        with winreg.OpenKey(base_hive, key_path) as key:
            values = {}
            subkeys = []

            # Legge i valori della chiave corrente
            i = 0
            while True:
                try:
                    value_name, value_data, _ = winreg.EnumValue(key, i)
                    values[value_name] = value_data
                    i += 1
                except OSError:
                    break

            # Elenca le sottochiavi
            i = 0
            while True:
                try:
                    subkey_name = winreg.EnumKey(key, i)
                    subkeys.append(subkey_name)
                    i += 1
                except OSError:
                    break

            # Stampa i valori della chiave corrente
            if values:
                print(f"[green]Valori trovati in {key_path}:[/green]")
                for name, data in values.items():
                    print(f"  {name}: {data}")

            # Ricorsivamente legge le sottochiavi
            for subkey in subkeys:
                subkey_path = os.path.normpath(f"{key_path}\\{subkey}")
                print(f"\n[yellow]Esplorando sottochiave: {subkey_path}[/yellow]")
                read_registry_recursive(subkey_path, base_hive)

    except FileNotFoundError:
        print(f"[red]Chiave non trovata: {key_path}[/red]")
    except PermissionError:
        print(f"[red]Permessi insufficienti per accedere a: {key_path}[/red]")
    except Exception as e:
        print(f"[red]Errore durante l'accesso a {key_path}: {e}[/red]")

def find_guids_in_cs_files(directory, search_text):
    guid_pattern = re.compile(r'Guid\("([A-Fa-f0-9-]+)"\)')
    guids = []

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.cs'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        for line in f:
                            if search_text in line:
                                match = guid_pattern.search(line)
                                if match:
                                    print(f"Found GUID inside file [magenta]{file_path}[/magenta]")
                                    guids.append(match.group(1))
                except Exception as e:
                    pass

    return guids

def main():
    parser = argparse.ArgumentParser(description="Trova GUID nei file .cs e verifica le chiavi di registro.")
    parser.add_argument("directory", type=str, help="Percorso iniziale della directory da scansionare")
    args = parser.parse_args()

    search_text = '[ComVisible(true), ClassInterface(ClassInterfaceType.None), Guid('
    guids_found = find_guids_in_cs_files(args.directory, search_text)

    base_paths = [
        r"SOFTWARE\Classes\CLSID",
        r"SOFTWARE\WOW6432Node\Classes\CLSID",
    ]

    for clsid in guids_found:
        for base_path in base_paths:
            key_path = os.path.normpath(f"{base_path}\\{{{clsid}}}")
            print(f"\nEsplorando [blue]CLSID: {clsid}[/blue] | Path = [blue]{key_path}[/blue]")
            read_registry_recursive(key_path)

if __name__ == "__main__":
    main()
