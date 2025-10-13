

import math
import random
import time
import threading
from typing import Tuple

import pyautogui
from pynput.mouse import Button, Controller
from data_center.models.auto_attack_model.state import AutoAttackModelState
from data_center.models.input_monitor.state import InputMonitorState

mouse = Controller()

# 快速点击 - 几乎没有延迟
# mouse.press(Button.left)
# mouse.release(Button.left)

# 或者直接用 click 方法（单次点击）
# mouse.click(Button.left, 1)

# 自动攻击锁（防止重复执行）
_auto_attack_lock = threading.Lock()


def auto_attack(selected_target_point: Tuple[float, float]):
    return 
    """
    自动攻击函数
    
    Args:
        selected_target_point: 目标点相对屏幕中心的偏移 (x, y)
    
    说明：
        - 当目标距离小于10像素时触发攻击
        - 使用锁机制防止重复执行
        - 如果上一次攻击还在执行中，则跳过本次
    """
    # 尝试获取锁（非阻塞）
    if not _auto_attack_lock.acquire(blocking=False):
        # 上一次攻击还在执行中，跳过本次
        print("上一次攻击还在执行中，跳过本次")
        return
    try:
        # 计算距离
        distance = math.hypot(selected_target_point[0], selected_target_point[1])
        # 距离小于10像素时执行攻击
        if distance < 10:
            AutoAttackModelState.get_state().is_attack.set(True)
            pyautogui.mouseDown()
            total_time = random.uniform(0.001, 0.06)
            time.sleep(0.05)
            pyautogui.mouseUp()
            total_time = random.uniform(0.156, 0.22)
            time.sleep(total_time)
            AutoAttackModelState.get_state().is_attack.set(False)
            AutoAttackModelState.get_state().is_track.set(False)
    finally:
        # 确保释放锁
        _auto_attack_lock.release()

# 自动追踪
def auto_track(selected_target_point: Tuple[float, float]):
    distance = math.hypot(selected_target_point[0], selected_target_point[1])
    print(f"距离: {selected_target_point} {distance}")
    if distance < 30:
        AutoAttackModelState.get_state().is_track.set(True)
    else:
        AutoAttackModelState.get_state().is_track.set(False)
    pass

if __name__ == "__main__":
    time.sleep(2)
    start_time = time.time()
    while True:
        auto_attack((0, 0))
        if time.time() - start_time > 5:
            break
    pass
