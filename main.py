# /usr/local/bin/python3.7.8

import time
from modules.utils.logger import logger as LOGGER
from modules.robot.robot import Robot
from modules.skill.skill_manager import SkillManager
from modules.uart.uart_connection import UartConnection


def main() -> bool:
    # 初始化
    robot = Robot()
    if not robot.init():
        LOGGER.error("ROBOT INIT FAILED.")
        return False
    
    skill_manager = SkillManager(robot)
    if not skill_manager.load_skills():
        LOGGER.error("技能加载失败")
        return False
    skill_manager.log_skills()
    
    # 技能指令处理函数
    def handler(command, skill_number = -1):
        if command == 0:
            # 关闭技能
            skill_manager.stop_skill()
        elif command == 1:
            skill_manager.start_skill(skill_manager)
        else:
            pass

    conn = UartConnection(handler)

    while True:
        pass

if __name__ == "__main__":
    LOGGER.info("程序开始运行")
    LOGGER.info("RESULT: " + str(main()))
    LOGGER.info("程序运行结束")
