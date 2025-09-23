from typing_extensions import Optional
from pydantic import ConfigDict
from data_center.models.base_state import BaseState, ReactiveVar


class PIDModel(BaseState):
    """
    PID模型状态类，管理PID相关参数和状态
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)
    kp: ReactiveVar[float | None] = 5  # 比例系数
    ki: ReactiveVar[float | None] = 0  # 积分系数
    kd: ReactiveVar[float | None] = 0.05  # 微分系数
    dt: ReactiveVar[float | None] = 0.02  # 采样时间

    output: ReactiveVar[tuple[float, float]] = None  # 输出
    error: ReactiveVar[tuple[float, float]] = None  # 误差
    is_enabled: ReactiveVar[bool] = False  # 是否启用

