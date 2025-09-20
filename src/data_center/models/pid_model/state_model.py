from typing_extensions import Optional
from pydantic import ConfigDict
from data_center.models.base_state import BaseState


class PIDModelState(BaseState):
    """
    PID模型状态类，管理PID相关参数和状态
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)
    kp: Optional[float] = None  # 比例系数
    ki: Optional[float] = None  # 积分系数
    kd: Optional[float] = None  # 微分系数

    last_error_x: Optional[float] = None  # 上一次x误差
    last_error_y: Optional[float] = None  # 上一次y误差
    last_output_x: Optional[float] = None # 上一次x输出
    last_output_y: Optional[float] = None # 上一次y输出


