import rich

try:
    from siscom.registry_search.file_reader import SearchTermFileReader
    from siscom.registry_search.key_value_printer import RegistryKeyValuePrinter
    from siscom.registry_search.search_service import RegistrySearchService
    from siscom.registry_search.tree_traverser import RegistryTreeTraverser
except ModuleNotFoundError:
    # Keep compatibility with direct module execution contexts.
    from registry_search.file_reader import SearchTermFileReader
    from registry_search.key_value_printer import RegistryKeyValuePrinter
    from registry_search.search_service import RegistrySearchService
    from registry_search.tree_traverser import RegistryTreeTraverser


class SearcherFacade:
    """Coordinate file loading and registry searches without changing legacy behavior."""

    def __init__(
        self,
        term_reader: SearchTermFileReader,
        search_service: RegistrySearchService,
    ) -> None:
        """Store dependencies used to read search terms and execute registry scans."""
        self._term_reader = term_reader
        self._search_service = search_service

    def search_from_file(self, file_path: str) -> None:
        """Read terms from file and run the same per-term search workflow as before."""
        strings = self._term_reader.read_terms(file_path)

        for term in strings:
            rich.print(f"\n[cyan]=== CERCA: '{term}' ===[/cyan]")
            self._search_service.search_registry_for_string(term)


_key_value_printer = RegistryKeyValuePrinter()
_tree_traverser = RegistryTreeTraverser(_key_value_printer)
_search_service = RegistrySearchService(_tree_traverser)
_term_reader = SearchTermFileReader()
_facade = SearcherFacade(_term_reader, _search_service)


def read_strings_from_file(file_path: str) -> list[str]:
    """Backward-compatible wrapper that reads non-empty lines from a UTF-8 file."""
    return _term_reader.read_terms(file_path)


def print_key_values(key, key_path) -> None:
    """Backward-compatible wrapper that prints values of an open registry key."""
    _ = key_path
    _key_value_printer.print_values(key)


def search_and_print_recursive(root, path: str) -> None:
    """Backward-compatible wrapper that prints a key and all recursive descendants."""
    _tree_traverser.print_subtree(root, path)


def search_registry_for_string(search_string: str) -> None:
    """Backward-compatible wrapper that searches all known root hives for a string."""
    _search_service.search_registry_for_string(search_string)


def searcher(file_path: str) -> None:
    """Entry point used by the CLI to search registry keys from a text file."""
    _facade.search_from_file(file_path)
