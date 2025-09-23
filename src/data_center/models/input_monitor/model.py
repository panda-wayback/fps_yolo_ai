from typing import Dict, Tuple
from typing_extensions import Optional
from pydantic import ConfigDict
from data_center.models.base_state import BaseState, ReactiveVar


class InputMonitorModel(BaseState):
    """鼠标驱动模型状态类"""
    # 配置参数
    mouse_left_click_time: ReactiveVar[float] = 0.0 # 鼠标左键点击时间
    mouse_right_click_time: ReactiveVar[float] = 0.0 # 鼠标右键点击时间
    keyboard_click_time: ReactiveVar[Dict[str, float]] = {} # 键盘按键时间

    