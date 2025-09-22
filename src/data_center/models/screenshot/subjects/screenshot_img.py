import numpy as np

def on_screenshot_img(img: np.ndarray):
    """截图图片变化时的回调函数"""
    print(f"screenshot_img: {img}")
    # 让yolo 识别图片
    # YoloSubject.send_detect(img)