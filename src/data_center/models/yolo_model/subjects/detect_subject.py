"""
YOLO检测话题处理
基于PID模型的最佳实践
"""

import numpy as np
from data_center.models.yolo_model.subject_model import YoloSubjectModel
from data_center.models.yolo_model.subject import YoloSubject


def get_state():
    from data_center.index import get_data_center
    return get_data_center().state.yolo_model_state


def set_detect_subject(img: np.ndarray = None):
    """处理YOLO检测"""
    if img is None:
        return
        
    try:
        result = get_state().model(img, verbose=False)
        YoloSubject.send_result(result)
    except Exception as e:
        print(f"YOLO检测错误: {e}")


def init_detect_subject():
    """初始化YOLO检测订阅"""
    YoloSubjectModel.detect_subject.subscribe(set_detect_subject)


init_detect_subject()


if __name__ == "__main__":
    # 测试用例
    import numpy as np
    test_img = np.zeros((300, 400, 3), dtype=np.uint8)
    YoloSubjectModel.detect_subject.on_next(test_img)