import ctypes
from typing import Tuple, Optional
import numpy as np
import cv2
from utils.logger.logger import log_time

SRCCOPY = 0x00CC0020

class ScreenCapturer:
    """
    高性能屏幕截图类，支持动态传入截图区域
    预先分配固定大小的资源缓存，避免频繁创建/销毁
    """
    def __init__(self, max_width: int = 320, max_height: int = 240):
        """
        初始化屏幕截图器
        
        Args:
            max_width: 支持的最大宽度，默认2560（支持2K屏）
            max_height: 支持的最大高度，默认1440
        注意：截图区域不能超过这个尺寸，否则会报错
        """
        # 创建设备上下文
        self.hdc = ctypes.windll.user32.GetDC(0)
        self.hdc_mem = ctypes.windll.gdi32.CreateCompatibleDC(self.hdc)
        
        # 固定缓存尺寸
        self.max_width = max_width
        self.max_height = max_height
        
        # 创建固定大小的 bitmap 和 buffer
        self.bitmap = ctypes.windll.gdi32.CreateCompatibleBitmap(
            self.hdc, self.max_width, self.max_height
        )
        ctypes.windll.gdi32.SelectObject(self.hdc_mem, self.bitmap)
        self.bits = ctypes.create_string_buffer(self.max_width * self.max_height * 4)
    
    def capture_screen(self, region: Optional[Tuple[int, int, int, int]] = None) -> np.ndarray:
        """
        截取屏幕指定区域
        
        Args:
            region: 截图区域，格式为 (left, top, right, bottom)
                   如果为 None，则截取整个屏幕
        
        Returns:
            截图的 numpy 数组，格式为 BGR
        """
        target_time = time.time()
        # 解析区域参数
        if region is None:
            w = ctypes.windll.user32.GetSystemMetrics(0)
            h = ctypes.windll.user32.GetSystemMetrics(1)
            left, top, width, height = 0, 0, w, h
        else:
            left, top, right, bottom = region
            width, height = right - left, bottom - top
        self.bits = ctypes.create_string_buffer(width * height * 4)

        # 截图到内存
        ctypes.windll.gdi32.BitBlt(self.hdc_mem, 0, 0, width, height,
                                   self.hdc, left, top, SRCCOPY)
        ctypes.windll.gdi32.GetBitmapBits(self.bitmap, len(self.bits), self.bits)
        # 转换为BGR格式（只读取实际需要的字节数）
        target_time = time.time()
        image = np.frombuffer(self.bits, dtype=np.uint8, count=width * height * 4)
        image = image.reshape((height, width, 4))
        return cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

    def release_resources(self):
        """释放所有资源"""
        ctypes.windll.gdi32.DeleteObject(self.bitmap)
        ctypes.windll.gdi32.DeleteDC(self.hdc_mem)
        ctypes.windll.user32.ReleaseDC(0, self.hdc)
    
    def __del__(self):
        """析构函数，自动释放资源"""
        try:
            self.release_resources()
        except:
            pass


if __name__ == '__main__':
    import time
    
    print("=" * 60)
    print("ScreenCapturer 持续截图测试")
    print("=" * 60)
    print("按 'q' 键退出")
    print()
    
    # 初始化截图器（默认支持2K分辨率）
    capturer = ScreenCapturer()
    
    # 定义几个测试区域
    test_regions = [
        (0, 0, 320, 240),      # 左上角
        None,                   # 全屏
    ]
    
    region_names = [
        "区域1: 左上角 (800x600)",
        "区域2: 中间偏左上 (800x600)",
        "区域3: 中间偏右下 (800x600)",
        "区域4: 全屏",
    ]
    
    current_region_idx = 0
    frame_count = 0
    start_time = time.time()
    last_fps_time = start_time
    fps = 0
    
    try:
        while True:
            time.sleep(0.01)
            # 获取当前测试区域
            current_region = test_regions[current_region_idx]
            
            # 截图
            target_time = time.time()
            img = capturer.capture_screen(current_region)
            print(f"时间: {int((time.time() - target_time) * 1000)}ms")
            
            # 计算FPS
            frame_count += 1
            

            
            # 显示图像
            cv2.imshow('Screen Capture Test', img)
            
            # 按键处理
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("\n\n退出测试...")
                break
            elif key == ord('s'):
                # 切换到下一个区域
                current_region_idx = (current_region_idx + 1) % len(test_regions)
                print(f"\n切换到: {region_names[current_region_idx]}")
    
    except KeyboardInterrupt:
        print("\n\n收到中断信号，退出测试...")
    
    finally:
        # 清理资源
        total_time = time.time() - start_time
        cv2.destroyAllWindows()
        capturer.release_resources()
        
        print()
        print("=" * 60)
        print(f"测试完成！总运行时间: {total_time:.2f} 秒")
        print("=" * 60)



