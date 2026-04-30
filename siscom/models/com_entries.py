"""Dataclasses used to represent COM entries from the Windows registry."""

from dataclasses import dataclass
from typing import Any


@dataclass
class ComDictEntry:
    """Raw registry entry composed of key path and collected name/value pairs."""

    registry_path: str
    values: dict[str, Any]


@dataclass
class ComEntry:
    """Formatted COM entry projected from relevant registry values."""

    registry_path: str
    class_name: str
    assembly: str
    codebase: str
    runtime_version: str
    threading_model: str

