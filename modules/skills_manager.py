from typing import List
from threading import Thread
from robomaster.robot import Robot
import os
import glob

SKILL_FUNCTION_TYPE = function[None, None]

# 技能管理类
class SkillManager:
    skills: List[SKILL_FUNCTION_TYPE]

    def __init__(self, robot: Robot):
        self.robot = robot
        self.skills = []

    def skill_id_builder(id: int):
        return "skill-" + id

    # 加载技能
    def load_skills(self) -> bool:
        # 获取当前skills目录内所有技能文件
        current_directory = os.getcwd()
        skill_file_names = glob.glob(current_directory + "/skills/*")

        for skill_file_name in skill_file_names:
            # 利用__import__函数动态导入技能并加载run函数至本类skills列表中
            skill = __import__("./skills/" + skill_file_name)
            try:
                skill_num = skill_file_name[0]
                skill_id = SkillManager.skill_id_builder(skill_num)
                self.skills[skill_id] = skill
            except Exception as e:
                # 加载失败
                print("请检查技能文件内run函数是否存在\n以下是报错信息:")
                print(e)
                return False
        # 加载成功
        return True

    # 启动指定技能
    # @param skill_id 技能id 
    # @return 返回启动是否成功
    def start_skill(self, skill_id: int) -> bool:
        skill = self.skills.get(SkillManager.skill_id_builder(skill_id))

        if skill is None:
            # 无此技能
            return False
        else:
            thread = Thread(target = skill, args=(self.robot))   
            thread.start()
            return True
