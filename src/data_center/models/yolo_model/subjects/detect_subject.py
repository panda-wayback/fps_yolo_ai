from rx.subject import Subject
from data_center.index import get_data_center

import numpy as np

from data_center.models.yolo_model.subject import YoloSubject

subject = Subject( )

def use_yolo_detect_subject(img:np.ndarray = None):
    subject.on_next(img)


def set_detect_subject(img:np.ndarray = None):
    result = YoloSubject.get_yolo_model_state().model.predict(img)
    YoloSubject.send_result(result)

def init_yolo_detect_subject():
    """初始化YOLO检测订阅"""
    subject.subscribe(set_detect_subject)

init_yolo_detect_subject()
        
if __name__ == "__main__":
    use_yolo_detect_subject(np.zeros((100, 100, 3), dtype=np.uint8))
    