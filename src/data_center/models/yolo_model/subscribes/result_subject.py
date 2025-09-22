"""
YOLO检测结果话题处理
基于PID模型的最佳实践
"""

from typing import List, Any

from data_center.models.target_selector.subject import TargetSelectorSubject



def send_result_to_target_selector(value: List[Any], selected_class_ids=None):
    """设置YOLO检测结果"""
    if not value:
        return
    print(f"send_result_to_target_selector ")
    
    # 如果传入了selected_class_ids，直接使用；否则让TargetSelectorSubject内部获取
    TargetSelectorSubject.send_yolo_results(value, selected_class_ids)
    pass


if __name__ == "__main__":
    # 测试用例
    pass