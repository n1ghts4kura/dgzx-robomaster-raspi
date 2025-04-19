# 日志实现
# 可以不看其实。

import os
import datetime
import logging
from logging import Logger

current_path = os.getcwd()
current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S").replace(":", "-")

log_filepath = f"{current_path}/assets/log/{current_datetime}.log"
with open(log_filepath, "x", encoding="utf-8") as f:
    pass

logger = logging.getLogger("logger")
formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")

cmd_output_handler = logging.StreamHandler()
file_output_handler = logging.FileHandler(log_filepath, mode="w", encoding="utf-8")
cmd_output_handler.setFormatter(formatter)
file_output_handler.setFormatter(formatter)

logger.setLevel(logging.DEBUG)
cmd_output_handler.setLevel(logging.DEBUG)
file_output_handler.setLevel(logging.DEBUG)

logger.addHandler(cmd_output_handler)
logger.addHandler(file_output_handler)

class MyLogger:
    def __init__(self, prefix: str):
        self.prefix: str    = prefix
        self.logger: Logger = logger

    def info(self, content: str):
        self.logger.info(self.prefix + content)
    
    def error(self, content: str):
        self.logger.error(self.prefix + content)

    def warning(self, content: str):
        self.logger.warning(self.prefix + content)

    def debug(self, content: str):
        self.logger.debug(self.prefix + content)

PREFIX_LIST = {
    "MAIN":                   "[main.py] ",
    "CLASS_RNDIS_CONNECTION": "[class RndisConnection] ",
}

def get_logger(identity: str):
    if identity not in PREFIX_LIST:
    	logger.error(f"Failed to create the logger identified with \"{identity}\".")
        return None
    return MyLogger(PREFIX_LIST[identity])

__all__ = ["get_logger", "PREFIX_LIST"]