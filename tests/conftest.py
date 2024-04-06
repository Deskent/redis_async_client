import sys
from pathlib import Path


# Path to testing source dir
src_path = str(Path(__file__).parent.parent / "src")
sys.path.append(src_path)

pytest_plugins = [
    "tests.fixtures",
]
