# /usr/local/bin/python3.7.8

from modules.utils.logger import logger as LOGGER
from modules.robot.robot import Robot
from modules.skill.skill_manager import SkillManager
from modules.rndis.rndis_connection import RndisConnection


def main() -> bool:
    # 初始化
    robot = Robot()
    if not robot.init():
        LOGGER.error("ROBOT INIT FAILED.")
        return False
    
    skill_manager = SkillManager(robot)
    if not skill_manager.load_skills():
        LOGGER.error("Failed to load skills")
        return False
    # skill_manager.log_skills()

    def handler(command: str, data: str):
        if command == "KEYBOARD":
            skill_manager.load_skills(data)

    rndis_conn = RndisConnection(handler)
    if not rndis_conn.initialize():
        LOGGER.error("Failed to connect to the socket.")
        return False

    rndis_conn.start()

    while True:
        pass


if __name__ == "__main__":
    LOGGER.info("程序开始运行")
    LOGGER.info("RESULT: " + str(main()))
    LOGGER.info("程序运行结束")
