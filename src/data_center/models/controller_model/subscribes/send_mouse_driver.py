import time
from typing import Tuple

from data_center.models.controller_model.state import ControllerModelState
from data_center.models.input_monitor.state import InputMonitorState
from data_center.models.mouse_driver_model.subject import MouseDriverSubject
from singleton_classes.controller.controller import get_controller
from utils.logger.logger import get_logger


def compute_mouse_driver(vector: Tuple[float, float]):

    current_time = time.time()
    max_submit_time = InputMonitorState.get_state().mouse_left_click_submit_time.get()  + InputMonitorState.get_state().mouse_left_click_time.get()
    print(f"current_time: {current_time}, max_submit_time: {max_submit_time}  {current_time > max_submit_time} {InputMonitorState.get_state().is_submit_vector.get()}")
    if current_time > max_submit_time and not InputMonitorState.get_state().is_submit_vector.get():
        return

    """计算鼠标驱动"""
    output = get_controller().compute(vector)
    get_logger().info(f"✅ {vector}  {output}  ControllerModel")
    ControllerModelState.get_state().output.set(output)
    pass

def send_mouse_driver(vector: Tuple[float, float]):
    """发送鼠标驱动"""
    try:
        MouseDriverSubject.send_vector(vector)
        print(f"✅ 发送鼠标驱动: {vector}")
    except Exception as e:
        print(f"❌ 发送鼠标驱动失败: {e}")
    pass