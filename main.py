from threading import Thread
from typing import List
import RPi.GPIO as GPIO

from modules.robot import Robot
from modules.skills_manager import SkillManager

SKILL_THREADS = List[Thread]

# 将技能加载进一个线程文件夹中
def load_skill_into_thread(robot: Robot, skill_manager: SkillManager) -> SKILL_THREADS:
    skills_threads = []
    skill_id = 1
    for skill in skill_manager.skills:
        # 创建线程
        thread = Thread(target=skill, args=(robot, skill_id), name="Thread-" + skill_id)
        skills_threads.append(thread)
        skill_id += 1
    return skills_threads

# 加载指定技能
def start_skill(skills_threads: SKILL_THREADS, skill_id: int) -> bool:
    for skill in skills_threads:
        if skill.name == "Thread-" + skill_id:
            skill.start()
            return True
    return False

# 使用到的8个GPIO口序号
# 使用BOARD编号
PIN_USED_LIST = (11, 12, 13, 15, 16, 18, 22, 29)

def main():
    # GPIO初始化
    GPIO.setmode(GPIO.BOARD)
    for pin in PIN_USED_LIST:
        GPIO.setup(pin, GPIO.IN)

    robot = Robot()
    skill_manager = SkillManager()

    if not skill_manager.load():
        print("技能加载失败。")
        return

    skills_threads = load_skill_into_thread(robot, skill_manager)

    while True:
        for pin_num in range(1, 9):
            if GPIO.input(pin_num) == GPIO.HIGH:
                start_skill(skills_threads, pin_num)

if __name__ == "__main__":
    main()