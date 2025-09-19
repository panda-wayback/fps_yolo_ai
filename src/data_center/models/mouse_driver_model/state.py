

from data_center.models.base_state import BaseState


class MouseDriverState(BaseState):
    vx: float = 0.0
    vy: float = 0.0
    smoothing: float = 0.4
    fps: int = 1000
    running: bool = False
    # 单个向量最大执行时间
    max_duration: float = 0.05
    # 减速系数
    decay_rate: float = 0.95
    pass