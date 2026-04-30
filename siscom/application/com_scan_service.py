"""Application service that executes the COM scanning workflow used by the CLI."""

import os
import winreg

import rich
from rich import print

from siscom.guid.guid_finder import GuidFinder
from siscom.models.com_entries import ComDictEntry, ComEntry
from siscom.output.com_presenter import ComPresenter
from siscom.registry.com_entry_mapper import ComEntryMapper
from siscom.registry.com_registry_reader import ComRegistryReader
from siscom.searcher import searcher


class ComScanService:
    """Run the same COM discovery pipeline currently exposed by the command line."""

    def __init__(
        self,
        guid_finder: GuidFinder,
        registry_reader: ComRegistryReader,
        entry_mapper: ComEntryMapper,
        presenter: ComPresenter,
    ) -> None:
        """Store dependencies required to execute the full scanning workflow."""
        self._guid_finder = guid_finder
        self._registry_reader = registry_reader
        self._entry_mapper = entry_mapper
        self._presenter = presenter

    def run(self, args) -> None:
        """Execute the workflow with argparse namespace values from the CLI."""
        if args.search_from_list:
            searcher(args.search_from_list)
            return

        if args.path:
            guids_found_all = self._guid_finder.find_guids_in_cs_files(args.path)
            seen = set()
            guids_found = [x for x in guids_found_all if not (x in seen or seen.add(x))]
            if args.export:
                self._guid_finder.export_guids_to_file(guids_found)
        elif args.list:
            guids_found_all = self._guid_finder.find_guid_in_list_file(args.list)
            seen = set()
            guids_found = [x for x in guids_found_all if not (x in seen or seen.add(x))]

        base_paths = [
            r"SOFTWARE\Classes\CLSID",
            r"SOFTWARE\WOW6432Node\Classes\CLSID",
        ]

        registry_paths = []

        for clsid in guids_found:
            for base_path in base_paths:
                key_path = os.path.normpath(f"{base_path}\\{{{clsid}}}")
                registry_paths.append(key_path)
                print(f"Registry path loaded: [green]{key_path}[/green]")

        com_entries: list[ComDictEntry] = []
        for item in registry_paths:
            self._registry_reader.read_registry_recursive(item, com_entries, winreg.HKEY_LOCAL_MACHINE, args.verbose)

        rich.print("\n\n\n")
        formatted_entries: list[ComEntry] = []
        for raw_entry in com_entries:
            if raw_entry.registry_path.endswith("InprocServer32"):
                formatted_com_entry = self._entry_mapper.format_com_entry(raw_entry)
                formatted_entries.append(formatted_com_entry)

        self._presenter.print_com_entries(formatted_entries)
        self._presenter.print_relevant_info_com_entries(formatted_entries)


def build_default_com_scan_service() -> ComScanService:
    """Create a fully wired service instance with production dependencies."""
    return ComScanService(
        guid_finder=GuidFinder(),
        registry_reader=ComRegistryReader(),
        entry_mapper=ComEntryMapper(),
        presenter=ComPresenter(),
    )

