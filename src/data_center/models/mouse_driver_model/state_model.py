from typing_extensions import Optional
from pydantic import ConfigDict
from data_center.models.base_state import BaseState


class MouseDriverState(BaseState):
    """鼠标驱动模型状态类"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    # 鼠标向量
    vx: float = 0.0
    vy: float = 0.0
    
    # 配置参数
    smoothing: float = 0.4          # 平滑系数
    fps: int = 1000                 # 帧率
    running: bool = False           # 运行状态
    max_duration: float = 0.05      # 单个向量最大执行时间
    decay_rate: float = 0.95        # 减速系数
