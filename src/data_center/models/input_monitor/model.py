from data_center.models.base_state import BaseState, ReactiveVar


class InputMonitorModel(BaseState):
    """鼠标驱动模型状态类"""
    # 配置参数

    mouse_right_click_time: ReactiveVar[float] = 0.0 # 鼠标右键点击时间
    keyboard_click_name: ReactiveVar[str] = ReactiveVar("") # 键盘按键名称

    # mouse left 点击后多长时间提交向量
    mouse_left_click_time: ReactiveVar[float] = 0.0 # 鼠标左键点击时间
    mouse_left_click_submit_time: ReactiveVar[float] = 0.8 # 鼠标左键点击后多长时间提交向量

    is_submit_vector: ReactiveVar[bool] = True # 是否提交向量