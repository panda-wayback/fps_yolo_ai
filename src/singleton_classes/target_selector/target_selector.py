#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
目标选择器 - 简洁版
从DataCenter获取数据并处理目标选择
"""

from threading import Lock
from typing import Any, List
from data_center.models.target_selector.state import TargetSelectorState
from utils.yolo.yolo_result_utils import select_best_target
# 延迟导入避免循环依赖
from data_center.models.yolo_model.state import YoloModelState
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
        # 参考向量
        self.reference_vector = None
        # 修复：移除未定义的类型和变量，添加类型注释说明
    
    def target_selector(self, yolo_result: List[Any]) :
        """目标选择器主函数"""

        
        selected_class_ids = YoloModelState.get_state().selected_class_ids.get()
        distance_weight = TargetSelectorState.get_state().distance_weight.get()
        similarity_weight = TargetSelectorState.get_state().similarity_weight.get()
        confidence_weight = TargetSelectorState.get_state().confidence_weight.get()
        class_weight = TargetSelectorState.get_state().class_weight.get()

        if not yolo_result:
            return None, None, None, None
           
        selected_target_point, selected_target_bbox, selected_target_confidence, selected_target_class_id  = select_best_target(
            yolo_result[0],
        )
        print(f"✅ selected_target_point  {selected_target_point} 目标选择器")
        return selected_target_point, selected_target_bbox, selected_target_confidence, selected_target_class_id    




_target_selector = TargetSelector()
def get_target_selector():
    return _target_selector


if __name__ == "__main__":
    # 测试代码
    print("=== TargetSelector 测试 ===")
    