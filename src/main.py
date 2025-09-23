"""
FPS游戏AI辅助主程序 - 最小示例
加载YOLO模型并检测鼠标周围的目标，显示截图和检测结果
"""

import time
import cv2
from pynput import keyboard
from singleton_classes.screenshot_img.main import MouseScreenshot

def init_state():
    from data_center.init_state import init_state
    init_state()
    pass

def load_yolo_model():
    from data_center.models.yolo_model.subject import YoloSubject
    YoloSubject.send_model_path("runs/aimlab_fast/weights/best.pt")
    pass

def load_screenshot():
    from singleton_classes.screenshot_img.main import get_screenshot
    screenshot = get_screenshot()
    screenshot.start()
    pass


def main():
    init_state()
    load_yolo_model()
    load_screenshot()

    pass


if __name__ == "__main__":
    main()
    time.sleep(100)