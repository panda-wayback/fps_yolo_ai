import numpy as np

from data_center.models.yolo_model.subject import YoloSubject

def on_screenshot_img(img: np.ndarray):
    if img is None:
        return
    """截图图片变化时的回调函数"""
    # 让yolo 识别图片
    YoloSubject.send_detect(img)