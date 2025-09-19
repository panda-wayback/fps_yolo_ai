from rx.subject import Subject

import numpy as np

from data_center.models.yolo_model.subjects.config import use_yolo_model_path_subject
from utils.screenshot_tool.mss_screenshot import capture_screenshot_bgr


subject = Subject( )

def get_state():
    from data_center.index import get_data_center
    return get_data_center().state.yolo_model_state

def use_yolo_detect_subject(img:np.ndarray = None):
    subject.on_next(img)


def set_detect_subject(img:np.ndarray = None):

    result = get_state().model(img , verbose=False)
    from data_center.models.yolo_model.subject import YoloSubject
    YoloSubject.send_result(result)

def init_yolo_detect_subject():
    """初始化YOLO检测订阅"""
    subject.subscribe( 
        set_detect_subject
    )

init_yolo_detect_subject()
        
if __name__ == "__main__":
    use_yolo_model_path_subject("runs/aimlab_fast/weights/best.pt")
    use_yolo_detect_subject(
        capture_screenshot_bgr()
    )
    