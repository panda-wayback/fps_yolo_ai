"""
YOLO检测结果话题处理
基于PID模型的最佳实践
"""

from typing import List, Any

from utils.logger.logger import log_time
from data_center.models.target_selector.subject import TargetSelectorSubject


def send_result_to_target_selector(value: List[Any]):
    """设置YOLO检测结果"""
    if not value:
        return
    # 如果传入了selected_class_ids，直接使用；否则让TargetSelectorSubject内部获取
    try:
        @log_time
        def send_yolo_results():
            TargetSelectorSubject.send_yolo_results(value)
        send_yolo_results()
    except Exception as e:
        print(f"❌ 发送YOLO检测结果到目标选择器失败: {e}")
    pass


if __name__ == "__main__":
    # 测试用例
    pass