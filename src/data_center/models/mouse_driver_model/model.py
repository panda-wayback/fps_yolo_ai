from typing import Tuple
from data_center.models.base_state import BaseState, ReactiveVar


class MouseDriverModel(BaseState):
    """鼠标驱动模型状态类"""
    

    # 配置参数
    smoothing: ReactiveVar[float] = 0.4          # 平滑系数
    fps: ReactiveVar[int] = 1000                 # 帧率
    interval: ReactiveVar[float] = 0.001          # 间隔
    max_duration: ReactiveVar[float] = 0.1      # 单个向量最大执行时间
    decay_rate: ReactiveVar[float] = 0.95        # 减速系数

    # 鼠标向量
    vector: ReactiveVar[Tuple[float, float]] = (0.0, 0.0)
    