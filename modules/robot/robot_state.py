from robomaster.robot import Robot

from ..utils.logger import logger as LOGGER

# 状态刷新频率
# 单位 Hz
# SUBSCRIBE_RATE = 5

# 机器人(EP)状态重置类
# 你现在看到的版本是纯阉割版
# 也就是说我放弃了对于机器人状态的监测与恢复
# 索性直接恢复到一切开始的状态
# 比如说云台回中 等等
# 等以后有上述要求了再实现吧。
# 具体内容请查看文档
# https://robomaster-dev.readthedocs.io/zh-cn/latest/python_sdk/robomaster.html#robomaster-chassis
# - n1ghts4kura 25/3/29
class RobotStateRestorer:

    def __init__(self, robot: Robot):
        self.robot = robot
    
    # 重置
    def restore(self):

        LOGGER.info("正在重置机器人状态...")

        # 1.底盘
        self.robot.chassis.drive_speed(0, 0)
        self.robot.chassis.stick_overlay(0)

        # 2.云台
        self.robot.gimbal.resume()
        self.robot.gimbal.recenter(180, 180).wait_for_completed()
        self.robot.gimbal.drive_speed(0, 0)

        LOGGER.info("重置完成")