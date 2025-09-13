import threading
import time
import numpy as np
from typing import Optional

from singleton_classes.data_center import DataCenter
from utils.screenshot_tool.mss_screenshot import get_screen_size
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
        
        # 获取屏幕尺寸
        self.screen_width, self.screen_height = get_screen_size()
        
        # 截图参数
        self.mouse_pos = (self.screen_width // 2, self.screen_height // 2)
        self.region = (200, 200)  # (width, height)
        self.interval = 0.1
        
        # 线程控制
        self._thread = None
        self._running = False
        
        # 最新截图
        self._latest_image = None
        
        self._initialized = True
    
    def start(self, mouse_pos: tuple, 
              region: tuple = (200, 200),
              interval: float = 0.02):
        """
        开始截图
        """
        # 停止之前的线程
        if self._running:
            self.stop()
            time.sleep(0.1)
        
        # 设置参数
        self.mouse_pos = mouse_pos
        self.region = region
        self.interval = interval
        
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
    
    def get_img(self) -> Optional[np.ndarray]:
        """
        获取最新截图
        """
        return self._latest_image
    
    def _screenshot_loop(self):
        """
        截图循环
        """
        while self._running:
            try:
                # 使用get_mouse_region_image函数进行截图
                image = get_mouse_region_image(
                    self.region[0],  # width
                    self.region[1],  # height
                    self.mouse_pos
                )
                self._latest_image = image
                
                # 更新数据中心
                DataCenter().update_state(screenshot_img=image)

                time.sleep(self.interval)
                
            except Exception as e:
                print(f"截图错误: {e}")
                time.sleep(0.1)


# 便捷函数
def get_screenshot() -> MouseScreenshot:
    return MouseScreenshot()

if __name__ == "__main__":
    
    screenshot = MouseScreenshot()
    screenshot.start((200, 200), (200, 200), 0.1)
    time.sleep(1)
    img = screenshot.get_img()
    if img is not None:
        print(f"截图成功，尺寸: {img.shape}")
    screenshot.stop()
    pass