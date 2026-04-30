"""Utilities for loading registry search terms from files."""
class SearchTermFileReader:
    """Read and normalize search terms from a UTF-8 text file."""
    def read_terms(self, file_path: str) -> list[str]:
        """Return non-empty lines stripped from the given file path."""
        with open(file_path, "r", encoding="utf-8") as handle:
            return [line.strip() for line in handle if line.strip()]
