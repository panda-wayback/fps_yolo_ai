import time
from rx.subject import Subject

import numpy as np

from data_center.models.yolo_model.subjects.config import use_yolo_model_path_subject
from utils.screenshot_tool.mss_screenshot import capture_screenshot_bgr
from utils.thread.utils import threaded


subject = Subject( )

def get_state():
    from data_center.index import get_data_center
    return get_data_center().state.yolo_model_state

def use_yolo_detect_subject(img:np.ndarray = None):
    subject.on_next(img)

last_time = 0
def set_detect_subject(img:np.ndarray = None):

    current_time = time.time()
    # print(f"图片时间戳: {int(current_time * 1000 % 1e9)}")
    result = get_state().model(img, verbose=False)
    global last_time
    # 识别时间
    print(f"{int(time.time() % 1e3)} 识别时间: {int( (time.time() -   current_time )* 1000 % 1e9)}")
    if current_time > last_time:
        last_time = current_time
    else:
        print(f"图片时间戳过旧，跳过检测 (当前: {int(current_time * 1000 % 1e9)}, 上次: {int(last_time * 1000 % 1e9)})")
        return
    

    from data_center.models.yolo_model.subject import YoloSubject
    YoloSubject.send_result(result )

def init_yolo_detect_subject():
    """初始化YOLO检测订阅"""
    subject.subscribe( 
        # threaded(set_detect_subject)
        set_detect_subject
    )

init_yolo_detect_subject()
        
if __name__ == "__main__":
    use_yolo_model_path_subject("runs/aimlab_fast/weights/best.pt")
    use_yolo_detect_subject(
        capture_screenshot_bgr()
    )
    