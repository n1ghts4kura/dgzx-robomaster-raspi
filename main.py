# /usr/local/bin/python3.7.8

from modules.utils.logger import logger as LOGGER
from modules.robot.robot import Robot
from modules.skill.skill_manager import SkillManager
from modules.conv_init.connect import uart  #神秘错误未存取有时间改一下
import threading


def main():
    # 初始化
    uart=uart()
    robot = Robot()
    skill_manager = SkillManager(robot)
    if not skill_manager.load_skills():
        LOGGER.error("技能加载失败")
        return 

    # 通信逻辑
    while True:
        uart.conv_init()
        if not skill_manager.start_skill(uart.skill_accept()):
            print("技能启动失败")
            continue
        while uart.heart() and threading.activeCount != 0:
            continue
        skill_manager.stop_skill()

    

if __name__ == "__main__":
    LOGGER.info("程序开始运行")
    main()
    LOGGER.info("程序运行结束")