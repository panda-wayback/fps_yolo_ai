#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
目标选择器 - 简洁版
从DataCenter获取数据并处理目标选择
"""

from threading import Lock
from typing import Any, List
from data_center.models.yolo_model.state import YoloModelState
from singleton_classes.simulation_move_mouse.simulation_move_mouse import get_mouse_simulator
from utils.yolo.yolo_result_utils import select_best_target
class TargetSelector:
    """目标选择器单例类"""
    
    _instance = None
    _lock = Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        pass
    
    def target_selector(self, yolo_result: List[Any]) :
        """目标选择器主函数"""

        if not yolo_result:
            return None, None, None, None
        
        selected_class_ids = YoloModelState.get_state().selected_class_ids.get() # 选中的类别ID列表
        reference_vector = (get_mouse_simulator().vx, get_mouse_simulator().vy) # 参考向量

        selected_target_point, selected_target_bbox, selected_target_confidence, selected_target_class_id  = select_best_target(
            yolo_result[0],selected_class_ids,reference_vector
        )

        print(f"✅ selected_target_point  {selected_target_point} 目标选择器")
        return selected_target_point, selected_target_bbox, selected_target_confidence, selected_target_class_id    




_target_selector = TargetSelector()
def get_target_selector():
    return _target_selector


if __name__ == "__main__":
    # 测试代码
    print("=== TargetSelector 测试 ===")
    