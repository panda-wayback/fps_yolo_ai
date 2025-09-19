import time
from rx.subject import BehaviorSubject
from data_center.index import get_data_center
from data_center.models.screenshot.state import ScreenshotState
import numpy as np

from data_center.models.yolo_model.subject import YoloSubject
from functions.ims_show import get_yolo_marked_image
from singleton_classes.yolo_recog.yolo_recog import YoloRecog
from utils.thread.utils import threaded, threaded_with_args

# 只监控图片变化的订阅
subject = BehaviorSubject(None)

def use_subject_img(img):
    subject.on_next(img)

def get_state():
    return get_data_center().state.screenshot_state

# 示例：图片变化监听器
def on_img_change(img):
    """图片变化时的回调函数"""
    if img is not None:
        print(f"检测到图片变化: {img.shape}")
        get_state().screenshot_img = img
        # 这里可以添加图片处理逻辑，比如YOLO识别
    else:
        print(f"图片被清空")

def detect_img(img):
    """检测图片"""
    try:
        YoloSubject.send_detect(img)
    except Exception as e:
        print(f"YOLO识别错误: {e}")

def subscribe_img_subject():
    # 订阅图片变化
    subject.subscribe(threaded(on_img_change))
    subject.subscribe(threaded(detect_img))
    print(f"✅ 订阅图片变化成功")

subscribe_img_subject()

if __name__ == "__main__":

    
    # 模拟图片更新
    fake_img1 = np.zeros((480, 640, 3), dtype=np.uint8)
    fake_img2 = np.ones((720, 1280, 3), dtype=np.uint8) * 255


