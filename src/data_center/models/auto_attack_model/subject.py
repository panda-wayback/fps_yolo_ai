"""
自动攻击相关的统一接口
"""

from typing import Tuple
from data_center.models.auto_attack_model.state import AutoAttackModelState


class AutoAttackSubject:

    """自动攻击主题类"""
    @staticmethod
    def update_track_point(point: Tuple[float, float]):
        """设置追踪点"""
        AutoAttackModelState.get_state().track_point.set(point)
    
    # TODO: 添加更多方法
    


if __name__ == "__main__":
    # 测试用例
    pass

