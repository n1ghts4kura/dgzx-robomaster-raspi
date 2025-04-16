from robomaster.robot import Robot

# 测试技能范例

# 在start函数中，你要编写技能的主要逻辑，比如让机器人旋转等等
def start(robot: Robot):
    robot.chassis.drive_speed(2, 0)
    #robot.get_module("chassis").drive_speed(2,1)
