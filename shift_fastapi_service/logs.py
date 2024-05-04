import logging
import os
from pathlib import Path

from shift_fastapi_service.exceptions import LoggingConfigException

LOG_DIR_NAME = "logs"
MAIN_LOG_NAME = "main.log"


def init_logging() -> None:
    p = Path(".")
    log_dir_path = p / LOG_DIR_NAME
    if not log_dir_path.exists():
        create_log_directory(log_dir_path)
    elif not log_dir_path.is_dir():
        print(
            f"{log_dir_path.absolute()} already exists and isn't a directory"
        )
        raise LoggingConfigException
    main_log_path = log_dir_path / MAIN_LOG_NAME
    logging.basicConfig(filename=main_log_path, level=logging.INFO)


def create_log_directory(path: Path) -> None:
    try:
        os.mkdir(path)
    except OSError as e:
        print(f"cat't create directory on {path}", e, end="\n")
        raise LoggingConfigException from e
