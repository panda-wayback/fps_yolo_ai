import numpy as np

from utils.screenshot_tool.mss_screenshot import capture_screenshot_bgr, get_screen_size

def get_mouse_region_image(width: int, height: int, mouse_pos: tuple = None) -> np.ndarray:
    """
    获取以鼠标为中心的区域图像
    
    参数:
        width (int): 区域宽度
        height (int): 区域高度
        mouse_pos (tuple, optional): 鼠标位置 (x, y)，如果不提供则自动获取
    
    返回:
        np.ndarray: 鼠标周围区域的图像，BGR格式
    
    示例:
        # 获取200x200的正方形区域（自动获取鼠标位置）
        image = get_mouse_region_image(200, 200)
        
        # 获取300x200的长方形区域（使用指定鼠标位置）
        image = get_mouse_region_image(300, 200, (500, 300))
        
        # 先获取鼠标位置，然后多次使用
        mouse_x, mouse_y = get_mouse_position()
        image1 = get_mouse_region_image(200, 200, (mouse_x, mouse_y))
        image2 = get_mouse_region_image(300, 300, (mouse_x, mouse_y))
    """
    # 获取鼠标位置：如果提供了位置则使用，否则自动获取
    if mouse_pos is not None:
        mouse_x, mouse_y = mouse_pos
    else:
        # 获取屏幕中心位置
        width, height = get_screen_size()
        mouse_x, mouse_y =  width // 2, height // 2
    
    # 计算截图区域的左上角坐标
    left = int(mouse_x - width // 2)
    top = int(mouse_y - height // 2)
    
    # 使用capture_screenshot_bgr截取指定区域
    region = (left, top, width, height)
    image = capture_screenshot_bgr(region)
    
    return image
