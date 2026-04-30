"""Formatting and printing support for registry key values."""

import winreg


class RegistryKeyValuePrinter:
    """Print all values found under an opened registry key."""

    def print_values(self, key) -> None:
        """Enumerate and print all values for the provided open registry key."""
        try:
            index = 0
            while True:
                name, value, _ = winreg.EnumValue(key, index)
                print(f"    {name} = {value}")
                index += 1
        except OSError:
            pass

