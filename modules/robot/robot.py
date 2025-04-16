from robomaster import robot

from ..utils.logger import logger as LOGGER

# 机器人连接管理类
class Robot:
    def __init__(self):
        pass

    def init(self) -> bool:
        try:
            self.instance = robot.Robot()
            self.instance.initialize(conn_type="rndis")

            LOGGER.info("<class>[Robot] 机器人版本: " + self.instance.get_version())
            return True
        except Exception as e:
            LOGGER.error(str(e))
        return False

    def __del__(self):
        self.instance.close()
