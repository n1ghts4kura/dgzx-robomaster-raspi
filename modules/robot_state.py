from robomaster.robot import Robot

# 状态刷新频率
# 单位 Hz
SUBSCRIBE_RATE = 5

# 机器人状态管理类
# 用于技能启动前的状态保存 与 技能结束后的状态恢复
# 要是想看懂这个类具体工作原理请自行移步文档同步阅读API部分
# 从底盘状态开始
# https://robomaster-dev.readthedocs.io/zh-cn/latest/python_sdk/robomaster.html#robomaster-action
# 注意：本类未经过测试 不保证能够正常运行 请辩证看待
# 注意：本类未完成 1. 基本功能没动呢。 2-仍需添加多线程锁功能
# TODO YOU NEED TO TEST THIS CLASS BRO.
# TODO ADD MULTI-THREADING LOCKING BRO.
class RobotStateRestorer:

    # 注意：在初始化函数内 所有的实例变量的类型都不一定如在这里定义如此 请自行判断
    #       （我懒得自己看类型了，反正没什么用处。） - n1ghts4kura
    def __init__(self, robot: Robot):

        # 1.底盘状态
        # self.chassis_attitude = {
        #     "yaw": 0,
        #     "pitch": 0,
        #     "roll": 0
        # }
        # robot.chassis.sub_attitude(SUBSCRIBE_RATE, self.sub_chassis_callback)

        # self.chassis_esc = {
        #     "speed": [],
        #     "angle": [],
        #     "timestamp": "",
        #     "state": ""
        # }
        # robot.chassis.sub_esc(SUBSCRIBE_RATE, self.sub_chassis_esc_callback)
        pass


    # 底盘状态订阅函数
    # def sub_chassis_callback(self, yaw, pitch, roll):
    #     self.chassis_attitude["yaw"] = yaw
    #     self.chassis_attitude["pitch"] = pitch
    #     self.chassis_attitude["roll"] = roll

    # # 底盘状态订阅函数 2
    # def sub_chassis_esc_callback(self, speed, angle, timestamp, state):
    #     self.chassis_esc["speed"] = speed
    #     self.chassis_esc["angle"] = angle
    #     self.chassis_esc["timestamp"] = timestamp
    #     self.chassis_esc["state"] = state