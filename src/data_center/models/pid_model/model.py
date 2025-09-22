from typing_extensions import Optional
from pydantic import ConfigDict
from data_center.models.base_state import BaseState, ReactiveVar


class PIDModel(BaseState):
    """
    PID模型状态类，管理PID相关参数和状态
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)
    kp: ReactiveVar[float | None] = None  # 比例系数
    ki: ReactiveVar[float | None] = None  # 积分系数
    kd: ReactiveVar[float | None] = None  # 微分系数

    output: ReactiveVar[tuple[float, float]] = None  # 输出
    error: ReactiveVar[tuple[float, float]] = None  # 误差

