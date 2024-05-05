import os
from pathlib import Path
from typing import Any, Generator
from unittest.mock import patch

import pytest

import shift_fastapi_service.logs as logs
from shift_fastapi_service.exceptions import LoggingConfigException

LOG_DIR = logs.LOG_DIR_NAME


@pytest.fixture
def path_with_log_dir_exists(
    temp_test_dir: Path,
) -> Generator[Path, Any, None]:
    dir_path = temp_test_dir / LOG_DIR
    try:
        os.mkdir(dir_path)
        print(f"{dir_path} created")
        yield temp_test_dir
    finally:
        os.rmdir(dir_path)
        print(f"{dir_path} removed")


@pytest.fixture
def file_on_log_dir_path(temp_test_dir: Path) -> Generator[Path, Any, None]:
    file_path = temp_test_dir / LOG_DIR
    try:
        with open(file_path, "a") as f:
            f.write("test\n")
        print(f"{file_path} created")
        yield file_path
    finally:
        os.remove(file_path)
        print(f"{file_path} removed")


class TestCreateLogDirectory:

    @pytest.fixture
    def log_dir(self, temp_test_dir: Path) -> Generator[Path, Any, None]:
        log_dir_path = temp_test_dir / LOG_DIR
        try:
            logs.create_log_directory(log_dir_path)
            yield log_dir_path
        finally:
            os.rmdir(log_dir_path)

    def test_log_dir_exists(self, log_dir: Path) -> None:
        assert log_dir.exists()

    def test_log_dir_is_dir(self, log_dir: Path) -> None:
        assert log_dir.is_dir()

    def test_on_os_error_raises(self, file_on_log_dir_path: Path) -> None:
        with pytest.raises(expected_exception=LoggingConfigException):
            logs.create_log_directory(path=file_on_log_dir_path)
        if file_on_log_dir_path.exists() and file_on_log_dir_path.is_dir():
            os.rmdir(file_on_log_dir_path)


class TestInitLogging:

    def test_log_dir_created(self, temp_test_dir: Path) -> None:
        root_dir_path: Path = temp_test_dir
        log_dir_path: Path = root_dir_path / LOG_DIR
        with patch(
            "shift_fastapi_service.logs.create_log_directory"
        ) as mock_func:
            logs.init_logging(log_root=root_dir_path)
        mock_func.assert_called_once_with(log_dir_path)

        if log_dir_path.exists() and log_dir_path.is_dir():
            os.rmdir(log_dir_path)

    def test_if_exists_log_dir_not_created(
        self, path_with_log_dir_exists: Path
    ) -> None:
        root_dir_path: Path = path_with_log_dir_exists
        with patch(
            "shift_fastapi_service.logs.create_log_directory"
        ) as mock_func:
            logs.init_logging(log_root=root_dir_path)
        mock_func.assert_not_called()
