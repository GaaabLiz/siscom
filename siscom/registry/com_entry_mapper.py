"""Mapping helpers that convert raw registry values into display-ready COM entries."""

from siscom.models.com_entries import ComDictEntry, ComEntry


class ComEntryMapper:
    """Map raw registry dictionaries into typed COM entry objects."""

    def format_com_entry(self, entry: ComDictEntry) -> ComEntry:
        """Create a formatted COM entry preserving legacy fallback values."""
        return ComEntry(
            class_name=entry.values["Class"] if "Class" in entry.values else "null",
            assembly=entry.values["Assembly"] if "Assembly" in entry.values else "null",
            codebase=entry.values["CodeBase"] if "CodeBase" in entry.values else "null",
            runtime_version=entry.values["RuntimeVersion"] if "RuntimeVersion" in entry.values else "null",
            threading_model=entry.values["ThreadingModel"] if "ThreadingModel" in entry.values else "null",
            registry_path=entry.registry_path,
        )

