# SISCOM 🔍

**SISCOM** is a Windows command-line tool that helps you audit **COM component registrations** in the Windows Registry.

Given a set of CLSIDs/GUIDs — extracted from C# source code or loaded from a plain text list — SISCOM queries the Windows Registry and shows you: which assemblies are registered, where they live, and which class names are tied to which codebases.

---

## What problem does it solve?

When you work on large .NET / COM interop projects you often need to answer questions like:

- *"Is this GUID actually registered on this machine?"*
- *"Which DLL/assembly is registered for this COM class?"*
- *"I have a list of GUIDs from source code — are they all present in the registry?"*

SISCOM automates all of this, so you don't have to poke around `regedit` manually.

---

## ⚙️ Requirements

- **Windows** (uses the Windows Registry — does not run on macOS/Linux)
- Python ≥ 3.11, **or** just download the pre-built `siscom.exe`

---

## 📦 Installation

### Option A — Pre-built executable (recommended for end users)

Download `siscom.exe` from the Releases page and place it anywhere on your `PATH`. That's it — no Python needed.

### Option B — Install from source (developers)

```bash
# Clone the repository
git clone https://github.com/your-org/siscom.git
cd siscom

# Create the virtual environment and install dependencies
make install-env        # uses uv under the hood

# Run directly
uv run python -m siscom.cli --help
```

---

## 🚀 Quick start examples

```bat
REM Scan a C# project folder and look up all found GUIDs in the registry
siscom.exe --path "C:\Projects\MyApp\src"

REM Same, but also save the discovered GUIDs to guids.txt
siscom.exe --path "C:\Projects\MyApp\src" --export

REM Load GUIDs from a hand-written list instead of scanning source code
siscom.exe --list "C:\myguids.txt"

REM Search the whole registry for any key whose path contains a string from a list
siscom.exe --search-from-list "C:\search_terms.txt"

REM Enable verbose output to see every key visited (including missing ones)
siscom.exe --path "C:\Projects\MyApp\src" --verbose
```

---

## 📖 CLI Arguments

| Argument | Value | Description |
|---|---|---|
| `--path PATH` | Directory path | Recursively scans all `.cs` files inside `PATH`, extracts every `Guid("…")` attribute, then queries the Windows Registry for each GUID found. |
| `--list FILE` | Text file path | Loads GUIDs line-by-line from `FILE` (one GUID per line) and queries the registry for each one. Use this when you already have a ready-made list. |
| `--search-from-list FILE` | Text file path | Searches the **entire Windows Registry** for any key path that contains one of the strings listed in `FILE` (one string per line). Unlike `--path`/`--list`, this mode does a full-registry scan and is not limited to COM CLSID paths. |
| `--export` | flag (no value) | Works together with `--path`. After scanning source files, writes all discovered GUIDs into `guids.txt` in the current working directory. |
| `--verbose` | flag (no value) | Prints detailed information for every registry key visited, including keys that were **not found** or produced a permission error. Useful for debugging. |
| `-h` / `--help` | — | Show the built-in help message and exit. |

> **Note:** `--path` and `--list` are mutually exclusive starting points. Use one or the other; if both are provided only `--path` is used.

---

## 📝 Input file formats

### `--list` — GUID list file

A plain UTF-8 text file with one GUID per line (curly braces are optional):

```
6B29FC40-CA47-1067-B31D-00DD010662DA
{9E66A290-4365-11D2-A997-00C04FA37DDB}
A4B544A1-438D-4B41-9325-869523E2D6C7
```

### `--search-from-list` — search terms file

A plain UTF-8 text file with one search string per line. SISCOM will highlight every registry key path that **contains** that string (case-insensitive):

```
MyCompany.MyPlugin
AcmeCorp
SomeAssemblyName
```

---

## 📊 Output

SISCOM prints results directly to the terminal using colour formatting:

- A **Rich table** listing each matched COM entry with columns:
  - `Registry Path` — full registry key
  - `Class Name` — the registered .NET class
  - `Assembly` — the assembly name and version
  - `Codebase` — path to the physical DLL on disk
- A **compact summary** line per entry: `ClassName → Codebase`

---

## 📁 Project structure

```
siscom/
├── cli.py                      ← CLI entry point (argument parsing only)
├── application/
│   └── com_scan_service.py     ← Main workflow orchestrator
├── guid/
│   └── guid_finder.py          ← GUID extraction from source files and lists
├── models/
│   └── com_entries.py          ← Data models (ComEntry, ComDictEntry)
├── output/
│   └── com_presenter.py        ← Terminal rendering (Rich tables)
├── registry/
│   ├── com_registry_reader.py  ← Windows Registry traversal
│   └── com_entry_mapper.py     ← Mapping raw values → ComEntry
└── registry_search/
    ├── search_service.py        ← Full-registry string search
    ├── tree_traverser.py        ← Recursive key printer
    ├── key_value_printer.py     ← Key value formatter
    └── file_reader.py           ← Search term loader
```

---

## 📜 Changelog

See [CHANGELOG.md](CHANGELOG.md) for the full release history.
