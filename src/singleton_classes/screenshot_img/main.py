import threading
import time

from data_center.models.auto_attack_model.state import AutoAttackModelState
from data_center.models.input_monitor.state import InputMonitorState
from data_center.models.screenshot.state import ScreenshotModelState
from data_center.models.screenshot.subject import ScreenshotSubject
from utils.logger.logger import log_time
from utils.screenshot_tool.mss_screenshot import capture_screenshot_bgr
from utils.singleton.main import singleton
import numpy as np


@singleton
class MouseScreenshot:
    """
    鼠标区域截图单例类
    内部线程不断截图，外部获取最新截图
    """
    
    def __init__(self):
        # 线程控制
        self._thread = None
        self._running = False
    
        
    def start(self):
        """
        开始截图
        """
        # 停止之前的线程
        if self._running:
            self.stop()
            time.sleep(0.1)
        
        # 启动线程
        self._running = True
        self._thread = threading.Thread(target=self._screenshot_loop, daemon=True)
        self._thread.start()
    
    def stop(self):
        """
        停止截图
        """
        self._running = False
        if self._thread:
            self._thread.join(timeout=1.0)

    def _screenshot_loop(self):
        """
        截图循环
        """
        @log_time
        def capture_screenshot():
            image = capture_screenshot_bgr(
                region=ScreenshotModelState.get_state().region.get()
            )
            return image
        
        @log_time
        def send_image(image: np.ndarray):
            ScreenshotSubject.send_image(image,time.time())

        while self._running:
            try:
                image = capture_screenshot()
                send_image(image)
            except Exception as e:
                print(f"截图错误: {e}")
            time.sleep(ScreenshotModelState.get_state().interval.get())

_screenshot = MouseScreenshot()

def get_screenshot():
    return _screenshot

if __name__ == "__main__":
    # from data_center.models.yolo_model.subject import YoloSubject
    # YoloSubject.send_model_path("runs/aimlab_fast/weights/best.pt")
    screenshot = get_screenshot()
    screenshot.start()
    time.sleep(2)
    pass


