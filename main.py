from src.functions import (
    change_versions,
    display_projects,
    input_new_version,
    load_projects,
    console,
)

def execution(new_version=None):
    projects = load_projects()
    display_projects(projects)

    if projects:
        if not new_version:
            new_version = input_new_version()
        change_versions(projects, new_version)
        console.print("[bold green]\nAll projects updated successfully![/bold green]")


if __name__ == "__main__":
    execution()
