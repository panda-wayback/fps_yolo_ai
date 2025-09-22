import threading
import time

from data_center.models.screenshot.state import ScreenshotModelState
from data_center.models.screenshot.subject import ScreenshotSubject
from utils.screenshot_tool.mss_screenshot import capture_screenshot_bgr


class MouseScreenshot:
    """
    鼠标区域截图单例类
    内部线程不断截图，外部获取最新截图
    """
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(MouseScreenshot, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        # 线程控制
        self._thread = None
        self._running = False
        self._initialized = True
    
        
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
        while self._running:
            try:
                image = capture_screenshot_bgr(ScreenshotSubject.get_state().region)
                begin_time = time.time()
                ScreenshotSubject.send_image(image)
                end_time = time.time()
                print(f"截图时间: {(end_time - begin_time)*1000}ms")
            
            except Exception as e:
                print(f"截图错误: {e}")
            
            time.sleep(ScreenshotModelState.get_state().interval)

_screenshot = MouseScreenshot()

def get_screenshot():
    return _screenshot

if __name__ == "__main__":
    from data_center.models.yolo_model.subject import YoloSubject
    YoloSubject.send_model_path("runs/aimlab_fast/weights/best.pt")
    screenshot = get_screenshot()
    screenshot.start()
    time.sleep(100)
    pass