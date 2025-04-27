import glob
import json
import re
from pathlib import Path
from rich.console import Console
from typing import List

# Initialize console
console = Console(highlight=False)


class Project:
    """Represents a .NET project with its assembly version information."""

    def __init__(self, name: str, path: str, version: str):
        self.name = name
        self.path = path
        self.version = version

    def __str__(self):
        return f"[{self.name}] {self.version}"

    def __repr__(self):
        return str(self)


def load_config() -> dict:
    """Loads the configuration from config.json."""
    config_path = Path("config.json")
    if not config_path.exists():
        raise FileNotFoundError(
            "Missing config.json! Please provide the configuration file."
        )
    with config_path.open(encoding="utf-8") as config_file:
        return json.load(config_file)


def load_projects() -> List[Project]:
    """Loads all projects matching the configured glob path."""
    config = load_config()
    path_glob = config["path_glob_assemblyinfo"]
    pattern = config["pattern_assemblyinfo"]
    projects = []

    # Identify the wildcard position in the glob pattern to extract the project name
    wildcard_index = [i for i, part in enumerate(path_glob.split("/")) if part == "*"]
    [0]

    for project_path in glob.glob(path_glob):
        assembly_file = Path(project_path)
        try:
            content = assembly_file.read_text(encoding="utf-8")
            version_match = re.search(pattern, content)
            if version_match:
                project_name = assembly_file.parts[wildcard_index]
                project_version = version_match.group(1)
                project = Project(project_name, str(assembly_file), project_version)
                console.log(f"Loaded project: {project.name}")
                projects.append(project)
            else:
                console.log(
                    f"[yellow]Warning: No version found in {assembly_file}[/yellow]"
                )
        except Exception as e:
            console.log(f"[red]Error reading {assembly_file}: {e}[/red]")

    return projects


def display_projects(projects: List[Project]) -> None:
    """Displays a summary of all projects."""
    if not projects:
        console.print("[bold red]No projects found.[/bold red]")
        return

    latest_version = max(
        projects, key=lambda p: [int(x) for x in p.version.split(".")]
    ).version

    console.print("\n[bold underline]Project Versions:[/bold underline]\n")
    for project in projects:
        color = "green" if project.version == latest_version else "cyan"
        console.print(
            f"[bold white]{project.name}[/bold white] - [bold {color}]{project.version}[/bold {color}]"
        )


def input_new_version() -> str:
    """Prompts the user to input a new valid version."""
    pattern = r"^\d+\.\d+\.\d+\.\d+$"
    console.print("\n")

    while True:
        new_version = console.input(
            "[bold blue]Enter a new version (format: X.X.X.X):[/bold blue] "
        )
        if re.match(pattern, new_version):
            return new_version
        console.print("[bold red]Invalid format! Please use X.X.X.X[/bold red]\n")


def change_versions(projects: List[Project], new_version: str) -> None:
    """Updates all projects' assembly versions to the new version."""
    config = load_config()
    pattern = config["pattern_assemblyinfo"]

    console.bell()

    for project in projects:
        assembly_file = Path(project.path)
        try:
            content = assembly_file.read_text(encoding="utf-8")
            updated_content = re.sub(
                pattern,
                f'[assembly: AssemblyVersion("{new_version}")]',
                content,
            )
            assembly_file.write_text(updated_content, encoding="utf-8")
            console.log(
                f"[green]Updated {project.name} to version {new_version}[/green]"
            )
        except Exception as e:
            console.log(f"[red]Error updating {project.name}: {e}[/red]")
