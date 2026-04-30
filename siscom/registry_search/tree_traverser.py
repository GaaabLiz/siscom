"""Recursive traversal utilities for Windows registry trees."""

import os
import winreg

import rich

from .key_value_printer import RegistryKeyValuePrinter


class RegistryTreeTraverser:
    """Traverse a registry key recursively and print all nested keys and values."""

    def __init__(self, key_value_printer: RegistryKeyValuePrinter) -> None:
        """Store the printer dependency used for key value output."""
        self._key_value_printer = key_value_printer

    def print_subtree(self, root, path: str) -> None:
        """Print the target key and recursively print all descendant keys."""
        try:
            key = winreg.OpenKey(root, path)
        except FileNotFoundError:
            return

        rich.print(f"\n[green][KEY] {path}[/green]")
        self._key_value_printer.print_values(key)

        try:
            index = 0
            while True:
                subkey_name = winreg.EnumKey(key, index)
                self.print_subtree(root, os.path.join(path, subkey_name))
                index += 1
        except OSError:
            pass
        finally:
            winreg.CloseKey(key)

