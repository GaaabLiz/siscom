"""Recursive readers for COM-related registry keys on Windows."""

import os
import winreg

from rich import print

from siscom.models.com_entries import ComDictEntry


class ComRegistryReader:
    """Read COM registry keys and collect raw entries used by the application."""

    def is_end_node(self, key_path: str) -> bool:
        """Return True when the path points to an InprocServer32 terminal key."""
        parts = key_path.split("\\")
        last = parts[-1]
        return last == "InprocServer32"

    def read_registry_recursive(
        self,
        key_path: str,
        entries: list[ComDictEntry],
        base_hive=winreg.HKEY_LOCAL_MACHINE,
        log: bool = False,
    ) -> None:
        """Collect key values recursively, preserving current traversal behavior."""
        try:
            with winreg.OpenKey(base_hive, key_path) as key:
                values = {}
                subkeys = []

                index = 0
                while True:
                    try:
                        value_name, value_data, _ = winreg.EnumValue(key, index)
                        values[value_name] = value_data
                        index += 1
                    except OSError:
                        break

                index = 0
                while True:
                    try:
                        subkey_name = winreg.EnumKey(key, index)
                        subkeys.append(subkey_name)
                        index += 1
                    except OSError:
                        break

                if values:
                    print(f"[green]Valori trovati in {key_path}:[/green]") if log else None
                    for name, data in values.items():
                        print(f"  {name}: {data}") if log else None

                entries.append(
                    ComDictEntry(
                        registry_path=key_path,
                        values=values,
                    )
                )

                for subkey in subkeys:
                    subkey_path = os.path.normpath(f"{key_path}\\{subkey}")
                    if self.is_end_node(subkey_path):
                        # Preserve legacy behavior: recursive call does not forward log.
                        self.read_registry_recursive(subkey_path, entries, base_hive)

        except FileNotFoundError:
            print(f"[red]Chiave non trovata: {key_path}[/red]") if log else None
        except PermissionError:
            print(f"[red]Permessi insufficienti per accedere a: {key_path}[/red]")
        except Exception as error:
            print(f"[red]Errore durante l'accesso a {key_path}: {error}[/red]")

