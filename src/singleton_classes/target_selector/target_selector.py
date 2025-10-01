#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
目标选择器 - 简洁版
从DataCenter获取数据并处理目标选择
"""

from typing import Any, List
from data_center.models.yolo_model.state import YoloModelState
from singleton_classes.simulation_move_mouse.simulation_move_mouse import get_mouse_simulator
from utils.yolo.yolo_result_utils import select_best_target
from utils.singleton.main import singleton


@singleton
class TargetSelector:
    """目标选择器单例类"""
    
    def __init__(self):
        pass
    
    def target_selector(self, yolo_result: List[Any]) :
        """目标选择器主函数"""
        try:
            if not yolo_result or len(yolo_result) == 0:
                print("❌ yolo_result 为空")
                return None, None, None, None
            
            selected_class_ids = YoloModelState.get_state().selected_class_ids.get() # 选中的类别ID列表
            reference_vector = (get_mouse_simulator().vx, get_mouse_simulator().vy) # 参考向量
            

            selected_target_point, selected_target_bbox, selected_target_confidence, selected_target_class_id  = select_best_target(
                yolo_result[0], reference_vector, selected_class_ids
            )

            print(f"✅ selected_target_point  {selected_target_point} 目标选择器")
            return selected_target_point, selected_target_bbox, selected_target_confidence, selected_target_class_id    
        except Exception as e:
            print(f"❌ 目标选择器失败: {e}")
            return None, None, None, None



_target_selector = TargetSelector()
def get_target_selector():
    return _target_selector


if __name__ == "__main__":
    # 测试代码
    print("=== TargetSelector 测试 ===")
    