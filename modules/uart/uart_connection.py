import threading
import serial
import time

from ..utils.logger import logger as LOGGER
from ..utils.logger import LOGGER_PREFIX as _p
LOGGER_PREFIX = _p["UART_CONNECTION"]

# 链接状态
# 正在连接中
CONNECTION_ING = 0x00
# 连接成功
CONNECTION_SUCCESS = 0x01

class UartConnection:

    # 初始化函数
    def __init__(
        self,
        # 数据处理函数 (command: int, skill_number: int = -1, ) -> None
        handler,
        # 配置串口
        # 具体串口请查询ubuntu系统内/dev/目录下挂载内容
        port: str     = "/dev/ttyAMA0",
        # 串口通信波特率 两边代码请同步
        baudrate: int = 115200,
        # 后面的其实我也不知道具体用处 两边代码同步即可
        bytesize: int = serial.EIGHTBITS,
        stopbits: int = serial.STOPBITS_ONE,
        parity:   int = serial.PARITY_NONE,
        timeout:  int = 3,  # 单位: seconds
    ):
        # self.port     = port
        # self.baudrate = baudrate
        # self.bytesize = bytesize
        # self.stopbits = stopbits
        # self.parity   = parity
        self.timeout  = timeout 
        self.handler  = handler

        # 串口通信类变量
        self.conn = serial.Serial(
            port     = port,
            baudrate = baudrate,
            bytesize = bytesize,
            parity   = parity,
            stopbits = stopbits,
            timeout  = timeout,
        )

        # 串口通信连接状态
        self.conn_status: int = CONNECTION_ING
        # 连接状态锁
        self.conn_status_lock: threading.Lock = threading.Lock()

        connection_thread = threading.Thread(target = self.loop, args = tuple())
        connection_thread.start()

    # 更改连接状态
    def set_status(self, status: int) -> bool:
        with self.conn_status_lock:
            if status == CONNECTION_ING or status == CONNECTION_SUCCESS:
                self.conn_status = status
                LOGGER.info(LOGGER_PREFIX + "修改uart连接模式为 {} 成功".format(status))
                return True
        return False

    # 获取连接状态
    def get_status(self) -> int:
        with self.conn_status_lock:
            return self.conn_status

    # 获取串口数据
    # 调用函数请保证conn连接成功
    def readline(self, size: int = -1) -> int:
        try:
            return int( self.conn.readline(size).decode("utf-8").strip() )
        except Exception as e:
            return -1
        
    # 发送串口数据
    # 调用函数请保证conn连接成功
    def sendline(self, text) -> bool:
        try:
            self.conn.write(str(text))
            return True
        except Exception as e:
            return False

    def loop(self):
        timer_start = time.time()
        timer_now   = time.time()
        while True:
            # 如果正在连接
            if self.get_status() == CONNECTION_ING:
                LOGGER.info(LOGGER_PREFIX + "uart开始连接")
                # 走正常初始化连接逻辑
                self.conn.close()
                self.conn.open()
                
                # 等待开启
                while not self.conn.is_open: pass

                # 发送握手数据包
                self.sendline(1001)
                # 若未接收到握手数据包证明未连接成功 继续等待握手数据包接收
                while True:
                    if self.readline() == 1001:
                        break
                # 已经接收到 进入正常监测流程
                self.set_status(CONNECTION_SUCCESS)
                LOGGER.info(LOGGER_PREFIX + "uart连接成功 进入正常监测流程")

            elif self.get_status() == CONNECTION_SUCCESS:
                # 正常监测流程 
                # 若接收到心跳包 刷新计时器
                if self.readline() == 1002:
                    timer_start = time.time()
                    LOGGER.info(LOGGER_PREFIX + "接收到心跳包")
                # 若接收到技能启动
                elif self.readline() == 1003:
                    # 接收技能序数
                    skill_number = self.readline()
                    LOGGER.info(LOGGER_PREFIX + "接收到指令 启动技能{}".format(skill_number))
                    self.handler(1, skill_number)
                else:
                    LOGGER.info(LOGGER_PREFIX + "请检查代码 错误位置于 接收到了未定义的串口数据")
                
                # 监测当前计时器时间 若超过5秒未接收则判定链接丢失 重新连接
                timer_now = time.time()

                if timer_now - timer_start >= 5000:
                    LOGGER.info(LOGGER_PREFIX + "连接丢失")
                    self.set_status(CONNECTION_ING)
                    self.handler(0)
                    continue
                
            else:
                LOGGER.info(LOGGER_PREFIX + "请检查代码 错误位置于 conn_status 变量取得了范围内的值")
