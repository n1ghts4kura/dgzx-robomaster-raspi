from robomaster import robot

from ..utils.logger import logger as LOGGER

# 机器人连接管理类
class Robot:
    instance: robot.Robot

    def __init__(self):
        self.instance = robot.Robot()
        self.instance.initialize(conn_type="rndis")

        LOGGER.info("机器人版本: " + self.instance.get_version)

    def __del__(self):
        self.instance.close()
