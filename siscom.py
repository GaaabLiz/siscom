import os
import re
import argparse

def find_guids_in_cs_files(directory, search_text):
    """
    Cerca ricorsivamente tutti i file .cs in una directory e trova i GUID nel testo specificato.

    :param directory: Percorso della directory da scansionare.
    :param search_text: Testo da cercare nei file.
    :return: Lista di GUID trovati.
    """
    guid_pattern = re.compile(r'Guid\("([A-Fa-f0-9-]+)"\)')
    guids = []

    # Cammina ricorsivamente attraverso la directory
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

def main():
    parser = argparse.ArgumentParser(description="Trova GUID nei file .cs.")
    parser.add_argument("path", type=str, help="Percorso iniziale della directory da scansionare")
    args = parser.parse_args()

    search_text = '[ComVisible(true), ClassInterface(ClassInterfaceType.None), Guid('
    guids_found = find_guids_in_cs_files(args.path, search_text)

    print(f"GUID trovati: {guids_found}")

if __name__ == "__main__":
    main()