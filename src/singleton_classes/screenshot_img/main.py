import threading
import time
import numpy as np
from typing import Optional

from data_center.models.screenshot.state import ScreenshotState
from data_center.models.screenshot.subject.img_subject import get_img_subject
from data_center.models.screenshot.subject.subject import get_screenshot_state_subject
from data_center.index import get_data_center
from data_center.models.yolo_model.subjects.result_subject import get_result_subject
from singleton_classes.yolo_recog.yolo_recog import YoloRecog
from utils.screenshot_tool.mss_screenshot import capture_screenshot_bgr, get_screen_size
from .utils.get_mouse_region_image import get_mouse_region_image


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
    
    def get_state(self):
        """获取当前截图状态"""
        return get_data_center().state.screenshot_state
    
    def update_config(self, mouse_pos:tuple=None, region_size:tuple=None, interval:float=None):
        """
        更新配置 - 只更新传入的参数
        
        Args:
            mouse_pos: 鼠标位置，不传则不更新
            region: 截图区域，不传则不更新  
            interval: 截图间隔，不传则不更新
        """
        get_screenshot_state_subject().on_next(ScreenshotState(mouse_pos=mouse_pos, region_size=region_size, interval=interval))
        
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
                image = capture_screenshot_bgr(self.get_state().region)

                self.process_img(image)

                time.sleep(self.get_state().interval)
                
            except Exception as e:
                print(f"截图错误: {e}")
                time.sleep(0.1)
    
    def process_img(self, img: np.ndarray):
        """
        处理截图
        """
        get_img_subject().on_next(img)
        pass

if __name__ == "__main__":
    
    screenshot = MouseScreenshot()
    screenshot.start((200, 200), (200, 200), 0.1)
    time.sleep(1)
    img = screenshot.get_img()
    if img is not None:
        print(f"截图成功，尺寸: {img.shape}")
    screenshot.stop()
    pass