import json
from random import randint
import pytest
import shutil


@pytest.fixture
def setup_test_environment(tmp_path):
    """Set up a temporary fake project environment for testing."""
    base_path = tmp_path / "Repos" / "C#Project"
    projects = ["ProjectAlpha", "ProjectBeta", "ProjectGamma"]

    random_version = (
        f"{randint(1, 99)}.{randint(1, 99)}.{randint(1, 99)}.{randint(1, 99)}"
    )

    assembly_info_content = f"""
using System.Reflection;

[assembly: AssemblyTitle("Example Project")]
[assembly: AssemblyDescription("")]
[assembly: AssemblyConfiguration("")]
[assembly: AssemblyCompany("Example Company")]
[assembly: AssemblyProduct("Example Product")]
[assembly: AssemblyCopyright("")]
[assembly: AssemblyTrademark("")]
[assembly: AssemblyCulture("")]
[assembly: AssemblyVersion("{random_version}")]
[assembly: AssemblyFileVersion("{random_version}")]
    """.strip()

    # Create files
    for project in projects:
        project_path = base_path / project / "Properties"
        project_path.mkdir(parents=True, exist_ok=True)
        with open(project_path / "AssemblyInfo.cs", "w", encoding="utf-8") as f:
            f.write(assembly_info_content)

    # Create config
    config_content = {
        "path_glob_assemblyinfo": "Repos/C#Project/*/Properties/AssemblyInfo.cs",
        "pattern_assemblyinfo": r'\[assembly:\s*AssemblyVersion\("(\d+\.\d+\.\d+\.\d+)"\)\]',
    }
    with open(project_path / "config.json", "w") as config_file:
        json.dump(config_content, config_file)

    yield tmp_path

    # Cleanup
    shutil.rmtree(tmp_path, ignore_errors=True)


@pytest.fixture
def setup_broken_environment(tmp_path):
    """Set up a temporary broken project environment for testing."""
    base_path = tmp_path / "Repos" / "C#Project"
    project_path = base_path / "BrokenProject" / "Properties"
    project_path.mkdir(parents=True, exist_ok=True)

    # Create a broken AssemblyInfo.cs (malformed version)
    broken_content = """
using System.Reflection;

[assembly: AssemblyTitle("Broken Project")]
[assembly: AssemblyVersion("1.0.0")  # Missing closing parenthesis
    """.strip()

    with open(project_path / "AssemblyInfo.cs", "w", encoding="utf-8") as f:
        f.write(broken_content)

    # Create valid config (because config file is unrelated to error in this case)
    config_content = {
        "path_glob_assemblyinfo": "Repos/C#Project/*/Properties/AssemblyInfo.cs",
        "pattern_assemblyinfo": r'\[assembly:\s*AssemblyVersion\("(\d+\.\d+\.\d+\.\d+)"\)\]',
    }
    with open(project_path / "config.json", "w") as config_file:
        json.dump(config_content, config_file)

    yield tmp_path

    # Cleanup
    shutil.rmtree(tmp_path, ignore_errors=True)
