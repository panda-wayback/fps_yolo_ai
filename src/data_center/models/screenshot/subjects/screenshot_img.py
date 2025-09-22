import numpy as np
from data_center.models.yolo_model.subject import YoloSubject

def on_screenshot_img(img: np.ndarray):
    """截图图片变化时的回调函数"""
    print(f"screenshot_img: {img}")

    YoloSubject.send_detect(img)