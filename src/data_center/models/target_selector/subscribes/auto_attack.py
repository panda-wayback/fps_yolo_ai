

import math
import time
import threading
from typing import Tuple

import pyautogui

from data_center.models.input_monitor.state import InputMonitorState


# 自动攻击锁（防止重复执行）
_auto_attack_lock = threading.Lock()


def auto_attack(selected_target_point: Tuple[float, float]):
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
        return
    
    try:
        # 计算距离
        distance = math.hypot(selected_target_point[0], selected_target_point[1])
        # 距离小于10像素时执行攻击
        if distance < 10:
            pyautogui.mouseDown()
            time.sleep(0.05)
            pyautogui.mouseUp()
            time.sleep(0.05)
    finally:
        # 确保释放锁
        _auto_attack_lock.release()

# 自动追踪
def auto_track(selected_target_point: Tuple[float, float]):
    distance = math.hypot(selected_target_point[0], selected_target_point[1])
    if distance < 30:
        InputMonitorState.get_state().is_submit_vector.set(True)
    pass