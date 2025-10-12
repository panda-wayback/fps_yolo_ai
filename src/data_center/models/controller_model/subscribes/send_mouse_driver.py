import math
import time
from typing import Tuple

from data_center.models.auto_attack_model.state import AutoAttackModelState
from data_center.models.controller_model.state import ControllerModelState
from data_center.models.input_monitor.state import InputMonitorState
from data_center.models.mouse_driver_model.subject import MouseDriverSubject
from singleton_classes.controller.controller import get_controller
from utils.logger.logger import get_logger


def compute_mouse_driver(vector: Tuple[float, float]):
    # left_click_submit_time = InputMonitorState.get_state().mouse_left_click_submit_time.get()
    # mouse_left_click_submit_time = InputMonitorState.get_state().mouse_left_click_time.get()
    # print(f"is_track: {AutoAttackModelState.get_state().is_track.get()}")
    # print(f"左键提交时间: {left_click_submit_time}")
    # print(f"鼠标左键点击时间: {mouse_left_click_submit_time} {left_click_submit_time + mouse_left_click_submit_time}  {time.time()}")
    # print(f"时间: {left_click_submit_time + mouse_left_click_submit_time > time.time()}")

    # if AutoAttackModelState.get_state().is_track.get() is False \
    #     and (left_click_submit_time + mouse_left_click_submit_time > time.time()) is False:
    #     return
    
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