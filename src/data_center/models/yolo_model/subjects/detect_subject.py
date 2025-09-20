"""
YOLO检测话题处理
基于PID模型的最佳实践
"""

import numpy as np
from data_center.index import get_data_center


def set_detect_subject(img: np.ndarray = None):
    """处理YOLO检测"""
    if img is None:
        return
    try:
        result = get_data_center().state.yolo_model_state.model(img, verbose=False)

        from data_center.models.yolo_model.subject import YoloSubject
        YoloSubject.send_result(result)
        
    except Exception as e:
        print(f"YOLO检测错误: {e}")


if __name__ == "__main__":
    # 测试用例
    import numpy as np
    test_img = np.zeros((300, 400, 3), dtype=np.uint8)
    from data_center.models.yolo_model.subject import YoloSubject
    YoloSubject.send_detect(test_img)