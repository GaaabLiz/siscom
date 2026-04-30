"""Command-line entry point for SISCOM tools."""

import argparse

from siscom.application.com_scan_service import build_default_com_scan_service


def build_parser() -> argparse.ArgumentParser:
    """Create and configure the CLI argument parser."""
    parser = argparse.ArgumentParser(description="Trova GUID nei file .cs e verifica le chiavi di registro.")
    parser.add_argument("--path", type=str, help="Percorso iniziale della directory da scansionare")
    parser.add_argument("--list", type=str, help="Percorso del file contenente la lista degli GUID.")
    parser.add_argument("--search-from-list", type=str, help="Percorso del file contenente la lista delle chiavi.")
    parser.add_argument("--export", action="store_true", help="Export to current directory all GIUD found in a .txt file.")
    parser.add_argument("--verbose", action="store_true", help="Log all entries found and not found.")
    return parser


def main() -> None:
    """Parse CLI arguments and run the application service."""
    parser = build_parser()
    args = parser.parse_args()
    service = build_default_com_scan_service()
    service.run(args)


if __name__ == "__main__":
    main()
