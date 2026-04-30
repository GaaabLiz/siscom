"""High-level orchestration for searching matching keys in Windows registry hives."""

import os
import winreg

from .tree_traverser import RegistryTreeTraverser


class RegistrySearchService:
    """Search registry hives for key paths containing a target string."""

    def __init__(self, traverser: RegistryTreeTraverser) -> None:
        """Store the traverser dependency used to print full matching subtrees."""
        self._traverser = traverser

    def search_registry_for_string(self, search_string: str) -> None:
        """Scan known roots and print each subtree whose key path contains the search string."""
        roots = {
            "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE,
            "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER,
            "HKEY_CLASSES_ROOT": winreg.HKEY_CLASSES_ROOT,
            "HKEY_USERS": winreg.HKEY_USERS,
            "HKEY_CURRENT_CONFIG": winreg.HKEY_CURRENT_CONFIG,
        }

        for root_name, root_const in roots.items():
            try:
                self._recursive_search(root_const, search_string)
            except Exception as error:
                print(f"Errore nel cercare in {root_name}: {error}")

    def _recursive_search(self, root, search_string: str, path: str = "") -> None:
        """Depth-first traversal that prints complete subtrees when a path matches."""
        try:
            key = winreg.OpenKey(root, path)
        except OSError:
            return

        if search_string.lower() in path.lower():
            self._traverser.print_subtree(root, path)

        try:
            index = 0
            while True:
                subkey_name = winreg.EnumKey(key, index)
                self._recursive_search(root, search_string, os.path.join(path, subkey_name))
                index += 1
        except OSError:
            pass
        finally:
            winreg.CloseKey(key)

