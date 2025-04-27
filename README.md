# Assembly Info Updater

## Description

The **Assembly Info Updater** is a Python-based tool that automates the process of updating the version number in `.cs` files, specifically `AssemblyInfo.cs`, used in C# projects. This tool can modify the version information in multiple projects at once, simplifying version management for large codebases.

This tool provides a flexible configuration system to define patterns for locating and updating version numbers. It supports multiple projects and can handle both correctly formatted and malformed version strings, providing warnings when issues are detected.

## Features

- Updates the version number in `AssemblyInfo.cs` files based on a given version.
- Supports multiple projects with flexible file path configuration.
- Provides error handling and warnings for malformed version strings.
- Can be easily extended and configured through a JSON configuration file.

## Requirements

- Python 3.7+
- `pytest` for testing

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run tests to ensure everything is set up correctly:
   ```bash
   pytest
   ```

## Usage

### Configuration

The tool uses a `config.json` file to define the following settings:

- **path_glob_assemblyinfo**: The glob pattern for locating `AssemblyInfo.cs` files.
- **pattern_assemblyinfo**: The regular expression pattern used to locate and update the version number in the files.

Example of `config.json`:

```json
{
    "path_glob_assemblyinfo": "Repos/C#Project/*/Properties/AssemblyInfo.cs",
    "pattern_assemblyinfo": "\\[assembly:\\s*AssemblyVersion\\(\"(\\d+\\.\\d+\\.\\d+\\.\\d+)\"\\)\\]"
}
```
### Updating Version

Run entry point `main.py`

```bash
python main.py
```

### Testing

Unit tests for this tool are written with `pytest`. To run the tests, simply execute:

```bash
pytest
```

The tests validate the version update functionality and check for error handling in malformed files.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.