# /usr/local/bin/python3.7.8

from modules.utils.logger import logger as LOGGER
from modules.robot.robot import Robot
from modules.skill.skill_manager import SkillManager


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


if __name__ == "__main__":
    LOGGER.info("程序开始运行")
    LOGGER.info("RESULT: " + str(main()))
    LOGGER.info("程序运行结束")
