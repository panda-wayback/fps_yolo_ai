import numpy as np
import time
from data_center.models.yolo_model.subject import YoloSubject

def on_screenshot_img(img: np.ndarray):
    if img is None:
        return
    """截图图片变化时的回调函数"""
    YoloSubject.send_detect(img)