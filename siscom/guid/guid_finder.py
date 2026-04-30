"""Services for finding, loading, and exporting GUID values."""

import os
import re

from rich import print


class GuidFinder:
    """Provide GUID discovery utilities for source files and text lists."""

    def find_guids_in_cs_files(self, directory: str) -> list[str]:
        """Scan a directory tree and return GUIDs found in C# Guid attributes."""
        guid_pattern = re.compile(r"Guid\(\s*\"([A-Fa-f0-9-]+)\"\s*\)")
        guids: list[str] = []

        for root, _, files in os.walk(directory):
            for file_name in files:
                if file_name.endswith(".cs"):
                    file_path = os.path.join(root, file_name)
                    try:
                        with open(file_path, "r", encoding="utf-8") as handle:
                            content = handle.read()
                            matches = guid_pattern.findall(content)
                            if matches:
                                for guid_value in matches:
                                    print(
                                        "Found [orange]GUID[/orange] in file "
                                        f"[magenta]{file_path}[/magenta]: {guid_value}"
                                    )
                                guids.extend(matches)
                    except Exception:
                        pass

        return guids

    def find_guid_in_list_file(self, file_path: str) -> list[str] | None:
        """Load GUID values from a plain text list file, one value per line."""
        lines: list[str] = []
        try:
            with open(file_path, "r") as file:
                for line in file:
                    lines.append(line.strip())
            return lines
        except FileNotFoundError:
            print(f"Il file {file_path} non è stato trovato.")
        except Exception as error:
            print(f"Si è verificato un errore: {error}")
        return None

    def export_guids_to_file(self, guids: list[str]) -> None:
        """Write GUID values to guids.txt in the current working directory."""
        try:
            with open("guids.txt", "w", encoding="utf-8") as file:
                for row in guids:
                    file.write(row + "\n")
            print("File scritto correttamente in guids.txt")
        except Exception as error:
            print(f"Si è verificato un errore: {error}")
