import time
import serial
import threading

from ..utils.logger import logger as LOGGER
from ..utils.logger import LOGGER_PREFIX as _p
from ..utils.logger import PREFIX_GENERATOR
_gen = PREFIX_GENERATOR(LOGGER_PREFIX = _p["UART_CONNECTION"])

CONN_STATUS_ING     = 0x00
CONN_STATUS_SUCCESS = 0x01

# 明文SDK通信连接类
class UartConnection:
    
    def __init__(
        self,
        # 指令处理函数
        handler,
        port     = "/dev/ttyAMA0",
        baudrate = 115200,
        bytesize = serial.EIGHTBITS,
        stopbits = serial.STOPBITS_ONE,
        parity   = serial.PARITY_NONE,
        timeout  = 5 # 单位: seconds
    ):
        self.set_status(CONN_STATUS_ING)

        self.conn_status = CONN_STATUS_ING
        self.conn_status_lock = threading.Lock()

        self.handler = handler
        
        # 配置串口
        _serial          = _serial.Serial()
        _serial.port     = port 
        _serial.baudrate = baudrate
        _serial.bytesize = bytesize
        _serial.stopbits = stopbits
        _serial.parity   = parity
        _serial.timeout  = timeout
        self.serial: serial.Serial = _serial

    def start(self):
        self.loop_thread = threading.Thread(target=self.loop, args=tuple())
        self.loop_thread.start()

    def writeline(self, content: str) -> bool:
        try:
            self.serial.write((content + "\n").encode("utf-8"))
        except:
            LOGGER.error(_gen("向串口写入数据失败"))
            return False
        return True

    def readline(self) -> str:
        try:
            response = self.serial.readline().decode("utf-8")
            response = response.strip()
        except:
            LOGGER.error(_gen("获取串口数据失败"))
            return False

        LOGGER.info(f"串口接收信息：{response}")
        return True

    # 初始化
    def initialize(self):
        # 连接
        count = 0

        self.serial.open()
        LOGGER.info(_gen("明文sdk开始连接"))
        while not self.serial.is_open:
            if count >= 10:
                LOGGER.error(_gen("明文sdk连接失败：串口无法连接。请重启程序"))
                return False
            count += 1
            time.sleep(1)

        self.writeline("command")
        if self.readline() != "ok":
            LOGGER.error(_gen("明文sdk初始化 command指令机器人端返回异常值"))
            return False

        LOGGER.info(_gen("明文sdk连接成功"))

        # 订阅数据
        self.writeline("game_msg on")

        self.set_status(CONN_STATUS_SUCCESS)
        return True

    def get_status(self) -> str:
        with self.conn_status_lock:
            return self.conn_status

    def set_status(self, status: str) -> bool:
        with self.conn_status_lock:
            if status not in (CONN_STATUS_ING, CONN_STATUS_SUCCESS):
                LOGGER.warning(_gen(f"设置连接状态为未定义值，具体值为：{status}"))
                return False
            LOGGER.info(_gen(f"设置连接状态为 {status}"))
            return True

    def loop(self):
        while True:
            if self.get_status() == CONN_STATUS_ING:
                self.initialize()
            elif self.get_status() == CONN_STATUS_SUCCESS:
                resp = self.readline()

                if "game msg push" in resp:
                    data = resp.split("[")[1].split("]")[0]
                    pressed_key = data[7]
                    pressed_key = int(pressed_key)

                    LOGGER.info(f"选手端 键盘按下：{pressed_key}")

                    self.handler("KEYBOARD", pressed_key)

            else:
                LOGGER.error(_gen("状态值异常，请检查代码。"))
                time.sleep(5)