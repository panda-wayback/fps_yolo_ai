"""
目标选择器相关的统一接口
基于PID模型的最佳实践
"""

from typing import Any, List, Optional, Tuple
from data_center.models.target_selector.state import TargetSelectorState

class TargetSelectorSubject:
    """目标选择器订阅统一接口"""
    
    @staticmethod
    def send_yolo_results(yolo_results: List[Any] ):
        """发送YOLO检测结果进行目标选择"""
        TargetSelectorState.get_state().yolo_results.set(yolo_results)
        pass

        

