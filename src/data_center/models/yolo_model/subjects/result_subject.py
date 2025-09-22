"""
YOLO检测结果话题处理
基于PID模型的最佳实践
"""

from data_center.index import get_data_center
from typing import List, Any, Optional, Dict

from data_center.models.target_selector.subject import TargetSelectorSubject



def send_result_to_target_selector(value: List[Any]):
    """设置YOLO检测结果"""
    try:
        
            TargetSelectorSubject.send_yolo_results(value)
            
    except Exception as e:
        print(f"设置YOLO检测结果错误: {e}")



if __name__ == "__main__":
    # 测试用例
    from data_center.models.yolo_model.subject import YoloSubject
    YoloSubject.send_result(None)