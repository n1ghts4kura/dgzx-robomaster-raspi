from threading import Thread
from typing import List
import RPi.GPIO as GPIO

from modules.robot import Robot
from modules.skills_manager import SkillManager

# 使用到的8个GPIO口序号
# 使用BOARD编号
PIN_USED_LIST = (11, 12, 13, 15, 16, 18, 22, 29)

def main():
    # GPIO初始化
    GPIO.setmode(GPIO.BOARD)
    for pin in PIN_USED_LIST:
        GPIO.setup(pin, GPIO.IN)

    robot = Robot()
    skill_manager = SkillManager(robot)
    if not skill_manager.load_skills():
        print("技能加载失败")
        return 

    while True:
        for pin_num in range(1, 9):
            if GPIO.input(pin_num) == GPIO.HIGH:
                skill_manager.start_skill(pin_num)

if __name__ == "__main__":
    main()