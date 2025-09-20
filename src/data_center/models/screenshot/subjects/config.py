"""
截图配置话题处理
基于PID模型的最佳实践
"""

from data_center.index import get_data_center
from data_center.models.screenshot.state_model import ScreenshotState
from data_center.models.screenshot.subject_model import ScreenshotSubjectModel
from utils.screenshot_tool.mss_screenshot import capture_screenshot_bgr


def set_screenshot_state_settings(value: ScreenshotState):
    """设置截图状态配置"""
    try:
        state = get_data_center().state.screenshot_state
        state.merge_state(value)
        
        # 计算截图区域和中心点
        if value.mouse_pos is not None and value.region_size is not None:
            # 截图区域
            state.region = (
                value.mouse_pos[0] - value.region_size[0] // 2,
                value.mouse_pos[1] - value.region_size[1] // 2,
                value.region_size[0],
                value.region_size[1]
            )
            # 截图图片中心点
            state.screen_center = (
                value.mouse_pos[0],
                value.mouse_pos[1]
            )
            
            print(f"✅ 截图配置已更新: mouse_pos={value.mouse_pos}, "
                  f"region_size={value.region_size}, fps={value.fps}")
            print(f"   计算区域: {state.region}, 中心点: {state.screen_center}")
        else:
            print(f"✅ 截图配置已更新: mouse_pos={value.mouse_pos}, "
                  f"region_size={value.region_size}, fps={value.fps}")
            
    except Exception as e:
        print(f"❌ 截图配置更新失败: {e}")


def init_config_subject():
    """初始化截图配置订阅"""
    ScreenshotSubjectModel.config_subject.subscribe(set_screenshot_state_settings)


init_config_subject()


if __name__ == "__main__":
    # 测试用例
    from utils.screenshot_tool.mss_screenshot import capture_screenshot_bgr
    
    img = capture_screenshot_bgr()
    ScreenshotSubjectModel.config_subject.on_next(
        ScreenshotState(
            mouse_pos=(100, 200),
            region_size=(100, 100),
            fps=30.0
        )
    )