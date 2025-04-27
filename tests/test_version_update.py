from main import execution
from pathlib import Path
from src.functions import load_config, load_projects
import pytest
import re

@pytest.mark.parametrize(
    "new_version",
    [
        "1.0.0.0",
        "1.2.3.4",
        "2.0.0.0",
        "2.5.1.0",
        "3.0.0.0",
        "3.1.4.1",
        "4.0.2.0",
        "4.5.6.7",
        "5.0.0.0",
        "5.10.15.20",
        "6.1.0.3",
        "7.2.1.4",
        "8.0.0.1",
        "9.9.9.9",
    ],
)
def test_version_updated(setup_test_environment, new_version: str):
    # Configuration
    config = load_config()
    pattern = config["pattern_assemblyinfo"]
    projects = load_projects()
    execution(new_version)

    # Check post execution
    for project in projects:
        content = Path(project).read_text(encoding="utf-8")
        version_match = re.search(pattern, content)
        if version_match:
            version_file = version_match.group(1)
            assert new_version == version_file