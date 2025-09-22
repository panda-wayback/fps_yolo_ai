#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
目标选择器 - 简洁版
从DataCenter获取数据并处理目标选择
"""

from threading import Lock

from data_center.models.yolo_model.subject import YoloSubject
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
        # 参考向量
        self.reference_vector = None
        # 修复：移除未定义的类型和变量，添加类型注释说明
    
    def target_selector(self, yolo_result) :
        """目标选择器主函数"""
        if not yolo_result:
            return None, None, None, None
        
        # 直接导入避免循环导入
        from data_center.index import get_data_center
        
        # 获取配置
        target_selector_state = get_data_center().state.target_selector_state
        yolo_state = YoloSubject.get_state()
           
        target = select_best_target(
            yolo_result,
            reference_vector = self.reference_vector,
            class_ids=yolo_state.selected_class_ids,
            distance_weight=target_selector_state.distance_weight,
            similarity_weight=target_selector_state.similarity_weight,
            confidence_weight=target_selector_state.confidence_weight,
            class_weight=target_selector_state.class_weight
        )

        if target:
            selected_point = target['center']
            selected_bbox = target['bbox']
            selected_confidence = target['confidence']
            selected_class_id = target['class_id']
            self.reference_vector = selected_point
            return selected_point, selected_bbox, selected_confidence, selected_class_id    
        else:
            self.reference_vector = None
            return None, None, None, None



_target_selector = TargetSelector()
def get_target_selector():
    return _target_selector


if __name__ == "__main__":
    # 测试代码
    print("=== TargetSelector 测试 ===")
    