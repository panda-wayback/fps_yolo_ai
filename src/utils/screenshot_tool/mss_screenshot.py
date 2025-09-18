import mss
import numpy as np
from typing import Tuple, Optional
import cv2


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
    with mss.mss() as sct:
        if region is None:
            # 如果没有指定区域，截取整个屏幕
            monitor = sct.monitors[1]  # monitors[0]是所有显示器的组合，monitors[1]是主显示器
        else:
            # 使用指定的区域
            left, top, width, height = region
            monitor = {
                "top": top,
                "left": left,
                "width": width,
                "height": height
            }
        
        # 执行截图
        screenshot = sct.grab(monitor)
        
        return screenshot


def capture_screenshot_bgr(region: Optional[Tuple[int, int, int, int]] = None) -> np.ndarray:
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
    
    # 移除alpha通道，只保留BGR
    if img_array.shape[2] == 4:  # 如果有alpha通道
        img_array = img_array[:, :, :3]  # 只取前3个通道(BGR)
    
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
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # 主显示器
        return monitor["width"], monitor["height"]


def get_all_monitors() -> list:
    """
    获取所有显示器的信息
    
    Returns:
        list: 所有显示器的信息列表
    """
    with mss.mss() as sct:
        return sct.monitors


if __name__ == "__main__":
    # 测试代码
    print("测试截图功能...")
    
    # 获取屏幕尺寸
    width, height = get_screen_size()
    print(f"屏幕尺寸: {width} x {height}")
    
    # 获取所有显示器信息
    monitors = get_all_monitors()
    print(f"显示器数量: {len(monitors)}")
    for i, monitor in enumerate(monitors):
        print(f"显示器 {i}: {monitor}")
    
    # 截取整个屏幕
    print("截取整个屏幕...")
    full_screenshot = capture_screenshot()
    print(f"截图尺寸: {full_screenshot.shape}")
    
    # 截取指定区域 (屏幕中心的一个小区域)
    center_x, center_y = width // 2, height // 2
    region_width, region_height = 400, 300
    left = center_x - region_width // 2
    top = center_y - region_height // 2
    
    print(f"截取区域: ({left}, {top}, {region_width}, {region_height})")
    region_screenshot = capture_screenshot((left, top, region_width, region_height))
    print(f"区域截图尺寸: {region_screenshot.shape}")
    
    # 保存截图
    print("保存截图...")
    success1 = save_screenshot("full_screenshot.png")
    success2 = save_screenshot("region_screenshot.png", (left, top, region_width, region_height))
    
    print(f"全屏截图保存: {'成功' if success1 else '失败'}")
    print(f"区域截图保存: {'成功' if success2 else '失败'}")
