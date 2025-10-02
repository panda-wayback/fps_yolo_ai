#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
目标选择器 - 简洁版
从DataCenter获取数据并处理目标选择
"""

from typing import Any, List, Optional, Tuple

from ultralytics.engine.results import Boxes
from utils.yolo.yolo_result_utils import select_best_target
from utils.singleton.main import singleton


@singleton
class TargetSelector:
    """目标选择器单例类"""
    
    def __init__(self):

        self.selected_target_id = None
        pass
    
    def target_selector(self, yolo_result: List[Any]) -> Optional[Tuple[Tuple[float, float], Boxes]]:
        """目标选择器主函数"""
       
        try:
            if not yolo_result or len(yolo_result) == 0:
                print("❌ yolo_result 为空")
                return None, None, None, None

            # 选择最佳目标
            vector_point, best_box = select_best_target(yolo_result[0], self.selected_target_id)

            self.selected_target_id = int(best_box.id.item())


            print(f"✅ 目标选择器 {vector_point}  {self.selected_target_id} ")
            return vector_point, best_box    
        except Exception as e:
            print(f"❌ 目标选择器失败: {e}")
            return None, None



_target_selector = TargetSelector()
def get_target_selector():
    return _target_selector


if __name__ == "__main__":
    # 测试代码
    print("=== TargetSelector 测试 ===")
    