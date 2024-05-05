import os
from pathlib import Path
from typing import Any, Generator

import pytest

TEST_DIR = "test_shift"


def create_test_dir(path: Path) -> None:
    try:
        os.mkdir(path)
    except OSError as e:
        print(f"cat't create directory on {path}", e, end="\n")


def remove_test_dir(path: Path) -> None:
    try:
        os.rmdir(path)
    except OSError as e:
        print(f"cat't remove directory on {path}", e, end="\n")


@pytest.fixture
def temp_test_dir() -> Generator[Path, Any, None]:
    if os.name == "posix":
        TEMP_DIR = Path("/tmp")
    elif os.name == "nt":
        TEMP_DIR = Path("C:/Windows/Temp")
    test_dir_path = TEMP_DIR / TEST_DIR
    try:
        create_test_dir(test_dir_path)
        yield test_dir_path
    finally:
        remove_test_dir(test_dir_path)
