from typing import Tuple
from data_center.models.pid_model.subject import PIDSubject
from singleton_classes.simulation_move_mouse.simulation_move_mouse import get_mouse_simulator
from utils.kalman.kaerman_fps import frame_step

def send_vector_to_pid(vector: Tuple[float, float]):
    """发送向量到PID"""
    # 获取鼠标模拟器的历史位移
    if vector is None:
        return
    displacement_history = get_mouse_simulator().get_displacement_history()
    # 使用卡尔曼滤波器处理向量
    # 参数顺序：frame_step(mouse_delta_pixels, detection)
    displacement_history_reverse  = (-displacement_history[0], -displacement_history[1])
    featured_vector = frame_step(displacement_history_reverse, vector)
    print(f"✅ 检测结果: {vector} -> 滤波后: {featured_vector} (鼠标移动: {displacement_history})")
    # 发送滤波后的向量到PID
    PIDSubject.send_update(vector)
