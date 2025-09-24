"""
截图配置话题处理
基于PID模型的最佳实践
"""

from typing import Tuple

def get_screenshot_state_settings(
    mouse_pos: Tuple[int, int],
    region_size: Tuple[int, int],
    fps: float
) -> Tuple[Tuple[int, int, int, int], Tuple[int, int], float]:
    """设置截图状态配置"""
    try:
        
        # 计算截图区域和中心点
        if mouse_pos is not None and region_size is not None:
            # 截图区域
            region = (
                mouse_pos[0] - region_size[0] // 2,
                mouse_pos[1] - region_size[1] // 2,
                region_size[0],
                region_size[1]
            )
            # 截图图片中心点
            screen_center = (
                mouse_pos[0],
                mouse_pos[1]
            )
            
            interval = 1.0 / fps
            return region, screen_center, interval
        else:
            return None, None, None
            
    except Exception as e:
        print(f"❌ 截图配置更新失败: {e}")



if __name__ == "__main__":
    # 测试用例
    pass