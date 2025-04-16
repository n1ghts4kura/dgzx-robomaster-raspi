# 日志实现
# 可以不看其实。

import os
import datetime
import logging

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

LOGGER_PREFIX = {
    "UART_CONNECTION": "[class UartConnection] ",
}
