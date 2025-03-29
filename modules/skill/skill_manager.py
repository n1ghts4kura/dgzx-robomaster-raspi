from typing import List
from threading import Thread, Lock
from robomaster.robot import Robot
import os
import glob

from ..utils.logger import logger as LOGGER
from ..robot.robot_state import RobotStateRestorer

SKILL_FUNCTION = function[..., None]

# 线程锁
# lock = Lock()

# 技能管理类
class SkillManager:

    def __init__(self, robot: Robot):

        self.robot: Robot = robot

        # 技能列表类型：
        # [
        #   start1, start2, start3, ...
        # ]
        self.skills: List[SKILL_FUNCTION] = [None for i in range(7)]
        self.threads: List[Thread] = [None for i in range(7)]

        # 目前正在运行的技能
        self.current_skill: int = -1

        # 机器人状态重置器
        self.robot_resetter: RobotStateRestorer = RobotStateRestorer(robot)

    # 加载技能
    def load_skills(self) -> bool:

        LOGGER.info("开始加载技能...")

        current_directory = os.getcwd()
        skill_sort = []

        # 获取存放技能位置的配置文件
        with open(current_directory + "/assets/skills_conf") as config_file:
            for line in config_file.readlines():
                skill_sort.append(line.strip())
        
        # 获取当前skills目录内所有技能文件
        skill_file_names = glob.glob(current_directory + "/skills/*")

        for skill_file_name in skill_file_names:
            # 获取文件名（无后缀）
            skill_file_name = skill_file_name.split(".py")[0]

            # 跳过没有装载的技能
            if not skill_file_name in skill_sort:
                continue
            
            for index in range(7):
                if skill_file_name == skill_sort[index]:
                    try:
                        # 利用__import__函数动态导入技能启动函数
                        start_function: SKILL_FUNCTION = __import__("./skills/" + skill_file_name).start
                        # 将技能序数与技能对应
                        self.skills[index] = start_function

                        LOGGER.info(f"技能-{skill_file_name} 加载成功！")
                    except Exception as e:
                        LOGGER.exception(str(e))
                        LOGGER.error("技能加载失败，请检查代码。")
                        LOGGER.error(f"问题出现于 技能文件-{skill_file_name}")
                        return False

        # 检查是否有技能空槽
        if None in self.skills:
            empty_count = self.skills.count(None)
            LOGGER.warning(f"出现{empty_count}个技能空槽，请检查你的代码。")
                    
        # 创建线程对象
        for index in range(7):
            skill = self.skills[index]
            # 跳过空技能
            if skill is None:
                continue
            self.threads[index] = Thread(target = skill, args=(self.robot))

        # 加载成功
        LOGGER.info("全部技能加载成功。")
        return True

    # 启动指定技能
    # @param index 技能序数，比如第一个、第二个
    # @return 技能启动结果
    #         如果正常返回True
    #         如果启动失败或技能为空技能返回False
    def start_skill(self, index: int) -> bool:

        LOGGER.info(f"正在启动{index}号技能。")

        # 如果技能已经启动那么禁止再次启动，不然会报错
        # 必须先停止技能再进行启动行为
        if index == self.current_skill:
            LOGGER.warning(f"技能{index}已经启动。")
            return False

        # 先检查index参数范围
        if index < 0 or index > 6:
            LOGGER.warning(f"index={index}，参数范围错误，停止加载技能。")
            return False

        thread = self.threads[index]
        # 空技能无法启动，判定为失败
        if thread is None:
            LOGGER.warning(f"启动的技能{index}为空技能，请注意。")
            return False

        # 启动
        thread.start()
        self.current_skill = index
        LOGGER.info(f"技能{index}启动成功。")
        return True

    # TODO 未完成
    # 停止目前正在执行的技能，并对机器人对象进行状态还原
    # @return 结束技能的结果
    def stop_skill(self) -> bool:

        LOGGER.info("正在结束正在运行的技能...")

        # 如果没有技能正在运行
        if self.current_skill == -1:
            LOGGER.warning("目前没有技能正在运行！")
            return False

        # 否则重置机器人
        self.robot_resetter.restore()
        self.current_skill = -1

        LOGGER.info("重置完成。")
        return True
