from robomaster import robot

# 机器人连接管理类
class Robot:
    instance: robot.Robot

    def __init__(self):
        self.instance = robot.Robot()
        self.instance.initialize(conn_type="rndis")

    def __del__(self):
        self.instance.close()
