from typing import List
import os
import glob

SKILL_FUNCTION_TYPE = function[None, None]

# 技能管理类
class SkillManager:
    skills: List[SKILL_FUNCTION_TYPE]

    def __init__(self):
        self.skills = []

    # 加载技能
    def load(self) -> bool:
        # 获取当前skills目录内所有技能文件
        current_directory = os.getcwd()
        skill_file_names = glob.glob(current_directory + "/skills/*")

        for skill_file_name in skill_file_names:
            # 利用__import__函数动态导入技能并加载run函数至本类skills列表中
            skill = __import__("./skills/" + skill_file_name)
            try:
                self.skills.append(skill.run)
            except Exception as e:
                # 加载失败
                print("请检查技能文件内run函数是否存在\n以下是报错信息：")
                print(e)
                return False
        # 加载成功
        return True
