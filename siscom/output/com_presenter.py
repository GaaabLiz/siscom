"""Output formatting for COM entries shown in the terminal."""

import rich
from rich.table import Table

from siscom.models.com_entries import ComEntry


class ComPresenter:
    """Render COM entries using Rich tables and compact lines."""

    def print_com_entries(self, entries: list[ComEntry]) -> None:
        """Print all formatted COM entries inside a Rich table."""
        table = Table(title="COM Entries")
        table.add_column("Registry Path", style="cyan", overflow="fold")
        table.add_column("Class Name", style="green")
        table.add_column("Assembly", style="yellow", overflow="fold")
        table.add_column("Codebase", style="magenta", overflow="fold")

        for entry in entries:
            table.add_row(
                entry.registry_path,
                entry.class_name,
                entry.assembly,
                entry.codebase,
            )

        rich.print(table)

    def print_relevant_info_com_entries(self, entries: list[ComEntry]) -> None:
        """Print a compact class-name to codebase projection for each COM entry."""
        for entry in entries:
            message = f"[green]{entry.class_name}[/green] -> [magenta]{entry.codebase}[/magenta]"
            rich.print(message)

