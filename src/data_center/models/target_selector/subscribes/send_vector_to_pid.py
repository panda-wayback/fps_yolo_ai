from typing import Tuple
from data_center.models.pid_model.subject import PIDSubject
from singleton_classes.simulation_move_mouse.simulation_move_mouse import get_mouse_simulator
from utils.kalman.kaerman_fps import frame_step

def send_vector_to_pid(vector: Tuple[float, float]):
    """发送向量到PID"""
    # 获取鼠标模拟器的历史位移
    displacement_history = get_mouse_simulator().get_displacement_history()
    # 使用卡尔曼滤波器处理向量
    featured_vector = frame_step(vector, displacement_history)
    # 发送向量到PID
    PIDSubject.send_update(featured_vector)
