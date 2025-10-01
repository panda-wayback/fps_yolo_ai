"""
鼠标向量话题处理
基于PID模型的最佳实践
"""

import time
from data_center.models.input_monitor.state import InputMonitorState
from singleton_classes.simulation_move_mouse.simulation_move_mouse import get_mouse_simulator


def submit_vector(vector: tuple[float, float]):
    """执行鼠标模拟器提交向量"""
    try:
        if not InputMonitorState.get_state().is_submit_vector.get():
            return
        get_mouse_simulator().submit_vector(vector)
    except Exception as e:
        print(f"❌ 鼠标向量提交失败: {e}")



if __name__ == "__main__":
    # 测试用例
    from data_center.models.mouse_driver_model.subject import MouseDriverSubject
    MouseDriverSubject.send_vector((1.0, 1.0))
