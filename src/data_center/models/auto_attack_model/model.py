from typing import Tuple
from data_center.models.base_state import BaseState, ReactiveVar


class AutoAttackModel(BaseState):
    """自动攻击模型状态类"""
    
    # 开关状态
    is_attack_enabled: ReactiveVar[bool] = False  # 是否启用自动攻击

    is_track: ReactiveVar[bool] = False  # 是否追踪

    is_attack: ReactiveVar[bool] = False  # 是否攻击

    track_point: ReactiveVar[Tuple[float, float]] = (0.0, 0.0)  # 追踪点
    
    # 攻击参数
    # TODO: 添加你需要的参数
    
    # 统计信息
    # TODO: 添加统计相关的字段

