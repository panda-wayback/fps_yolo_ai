import time
from rx.subject import BehaviorSubject
from data_center.index import get_data_center
from data_center.models.screenshot.state import ScreenshotState
import numpy as np

from data_center.models.yolo_model.subjects.result_subject import get_yolo_result_subject
from functions.ims_show import get_yolo_marked_image
from singleton_classes.yolo_recog.yolo_recog import YoloRecog
from utils.thread.utils import threaded, threaded_with_args

# 只监控图片变化的订阅
img_subject = BehaviorSubject(None)
def get_img_subject():
    return img_subject

state = get_data_center().state.screenshot_state


count = 0
# 示例：图片变化监听器
def on_img_change(img):
    """图片变化时的回调函数"""
    global count
    count += 1
    print(f"count: {count}")
    index = count 
    time.sleep(5 - count)

    if img is not None:
        print(f"检测到图片变化: {index} {img.shape}")
        state.screenshot_img = img
        # 这里可以添加图片处理逻辑，比如YOLO识别
    else:
        print(f"图片被清空: {index}")

def yolo_detect(img):
    """YOLO识别"""
    result = YoloRecog().detect(img)

    get_yolo_result_subject().on_next(result)

    marked_img = get_yolo_marked_image(img, result)

    state.marked_img = marked_img

if __name__ == "__main__":
    # 订阅图片变化
    img_subject.subscribe(
        threaded(
            on_img_change
        )
    )
    # img_subject.subscribe(yolo_detect)
    
    # 模拟图片更新
    fake_img1 = np.zeros((480, 640, 3), dtype=np.uint8)
    fake_img2 = np.ones((720, 1280, 3), dtype=np.uint8) * 255
    

    img_subject.on_next(fake_img1)
    img_subject.on_next(fake_img2)
    img_subject.on_next(None)  # 清空图片

    time.sleep(10)
