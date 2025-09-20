"""
YOLO检测结果话题处理
基于PID模型的最佳实践
"""

from data_center.index import get_data_center
from typing import List, Any, Optional, Dict

# 定义YOLO检测结果的类型
YoloDetection = Dict[str, Any]  # 单个检测结果
YoloResults = List[YoloDetection]  # YOLO检测结果列表


def set_result_subject(value: Optional[YoloResults] = None):
    """设置YOLO检测结果"""
    try:
        # 检测结果
        get_data_center().state.yolo_model_state.yolo_results = value
        # 标记图片
        if value and len(value) > 0:
            get_data_center().state.yolo_model_state.marked_img = value[0].plot()
    except Exception as e:
        print(f"设置YOLO检测结果错误: {e}")




if __name__ == "__main__":
    # 测试用例
    from data_center.models.yolo_model.subject import YoloSubject
    YoloSubject.send_result(None)