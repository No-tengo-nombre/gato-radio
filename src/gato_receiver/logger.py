from gato.configs import __BASE_DIR__
from datetime import datetime
import logging
import os


LOGGER = logging.Logger("gato_logger")

log_fmt = logging.Formatter(
    fmt="[%(asctime)s] %(levelname)s :: %(message)s",
    datefmt="%Y-%m-%d|%H:%M:%S",
)

# Stream logger
str_hdl = logging.StreamHandler()
str_hdl.setFormatter(log_fmt)
str_hdl.setLevel(logging.WARNING)
LOGGER.addHandler(str_hdl)

# File logger
now = datetime.now()
file_name = f"{now.year}{now.month:02}{now.day:02}_{now.hour:02}{now.minute:02}{now.second:02}"
file_path = os.path.join(__BASE_DIR__, "logs", f"{file_name}.txt")
file_hdl = logging.FileHandler(file_path, encoding="utf-8")
file_hdl.setFormatter(log_fmt)
file_hdl.setLevel(logging.DEBUG)
LOGGER.addHandler(file_hdl)

LOGGER.debug(f"Log file: {os.path.abspath(file_path)}")
