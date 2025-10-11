import mss
import numpy as np
from typing import Tuple, Optional
import cv2

# 创建全局的mss对象，复用以提高性能
# 避免每次截图都创建/销毁对象，提升连续截图速度
_sct = mss.mss()


def capture_screenshot(region: Optional[Tuple[int, int, int, int]] = None) -> np.ndarray:
    """
    使用MSS库进行屏幕截图
    
    Args:
        region: 截图区域，格式为 (left, top, width, height)
               如果为None，则截取整个屏幕
    
    Returns:
        np.ndarray: 截图的numpy数组，格式为BGR
    
    Example:
        # 截取整个屏幕
        screenshot = capture_screenshot()
        
        # 截取指定区域 (x=100, y=100, width=800, height=600)
        screenshot = capture_screenshot((100, 100, 800, 600))
    """
    # 使用全局的mss对象，避免重复创建
    if region is None:
        # 如果没有指定区域，截取整个屏幕
        monitor = _sct.monitors[1]  # monitors[0]是所有显示器的组合，monitors[1]是主显示器
    else:
        # # 使用指定的区域
        # left, top, width, height = region
        left, top, width, height = region
        monitor = {
            "top": top,
            "left": left,
            "width": width,
            "height": height
        }
    # 执行截图
    screenshot = _sct.grab(monitor)
    
    return screenshot




def capture_screenshot_bgr(region: Optional[Tuple[int, int, int, int]] = None
        ) -> np.ndarray:
    """
    使用MSS库进行屏幕截图，返回BGR格式的numpy数组
    
    Args:
        region: 截图区域，格式为 (left, top, width, height)
               如果为None，则截取整个屏幕
    
    Returns:
        np.ndarray: 截图的numpy数组，格式为BGR
    """

    screenshot = capture_screenshot(region)

        # 将PIL图像转换为numpy数组
    # MSS返回的是BGRA格式，我们需要转换为BGR
    img_array = np.array(screenshot)
    img_array = cv2.cvtColor(img_array, cv2.COLOR_BGRA2BGR)
    
    return img_array
    # return capture_screenshot(region)


def capture_screenshot_rgb(region: Optional[Tuple[int, int, int, int]] = None) -> np.ndarray:
    """
    使用MSS库进行屏幕截图，返回RGB格式的numpy数组
    
    Args:
        region: 截图区域，格式为 (left, top, width, height)
               如果为None，则截取整个屏幕
    
    Returns:
        np.ndarray: 截图的numpy数组，格式为RGB
    """
    bgr_img = capture_screenshot_bgr(region)
    # 将BGR转换为RGB
    rgb_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
    return rgb_img


def save_screenshot(filename: str, region: Optional[Tuple[int, int, int, int]] = None) -> bool:
    """
    截图并保存到文件
    
    Args:
        filename: 保存的文件名
        region: 截图区域，格式为 (left, top, width, height)
               如果为None，则截取整个屏幕
    
    Returns:
        bool: 保存是否成功
    """
    try:
        screenshot = capture_screenshot(region)
        # 使用OpenCV保存图像
        success = cv2.imwrite(filename, screenshot)
        return success
    except Exception as e:
        print(f"保存截图失败: {e}")
        return False


def get_screen_size() -> Tuple[int, int]:
    """
    获取屏幕尺寸
    
    Returns:
        Tuple[int, int]: (width, height)
    """
    # 使用全局mss对象
    monitor = _sct.monitors[1]  # 主显示器
    return monitor["width"], monitor["height"]


def get_all_monitors() -> list:
    """
    获取所有显示器的信息
    
    Returns:
        list: 所有显示器的信息列表
    """
    # 使用全局mss对象
    return _sct.monitors


if __name__ == "__main__":
    import time
    
    # 测试代码
    print("="*50)
    print("测试截图功能...")
    print("="*50)
    
    # 获取屏幕尺寸
    width, height = get_screen_size()
    print(f"屏幕尺寸: {width} x {height}")
    
    # 获取所有显示器信息
    monitors = get_all_monitors()
    print(f"显示器数量: {len(monitors)}")
    
    # 性能测试 - 连续截图100次
    print("\n【性能测试】连续截图100次...")
    test_region = (100, 100, 200, 200)
    
    start_time = time.time()
    for i in range(100):
        screenshot = capture_screenshot_bgr(test_region)
    elapsed = time.time() - start_time
    
    print(f"耗时: {elapsed:.3f}秒")
    print(f"平均每帧: {elapsed/100*1000:.2f}ms")
    print(f"理论最大FPS: {100/elapsed:.1f}")
    print(f"截图尺寸: {screenshot.shape}")
    
    print("\n✅ 使用全局_sct对象，避免重复创建，性能已优化！")
