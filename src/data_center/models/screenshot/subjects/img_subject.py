import time
from rx.subject import BehaviorSubject
from data_center.index import get_data_center
from data_center.models.screenshot.state import ScreenshotState
import numpy as np

from utils.thread.utils import threaded

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
        # print(f"检测到图片变化: {img.shape}")
        get_state().screenshot_img = img
    else:
        print(f"图片被清空")

def detect_img(img):
    """检测图片"""
    from data_center.models.yolo_model.subject import YoloSubject
    try:
        YoloSubject.send_detect(img)
    except Exception as e:
        print(f"YOLO识别错误: {e}")

def subscribe_img_subject():
    # 订阅图片变化 - 使用独立线程确保并行处理
    # subject.subscribe(threaded(on_img_change))  # 图片保存 - 轻量级任务
    # subject.subscribe(threaded(detect_img))     # YOLO检测 - 重量级任务
    subject.subscribe(on_img_change)  # 图片保存 - 轻量级任务
    subject.subscribe(detect_img)     # YOLO检测 - 重量级任务
    print(f"✅ 订阅图片变化成功")

subscribe_img_subject()

if __name__ == "__main__":

    
    # 模拟图片更新
    fake_img1 = np.zeros((480, 640, 3), dtype=np.uint8)
    fake_img2 = np.ones((720, 1280, 3), dtype=np.uint8) * 255


