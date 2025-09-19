from rx.subject import BehaviorSubject
from data_center.index import get_data_center
from data_center.models.screenshot.state import ScreenshotState
import numpy as np

from utils.screenshot_tool.mss_screenshot import capture_screenshot_bgr

subject = BehaviorSubject(ScreenshotState(
    interval=0.001
))
state = get_data_center().state.screenshot_state

def get_screenshot_config_subject():
    return subject

def use_screenshot_config_subject(
    mouse_pos: tuple[int, int] = None,
    region_size: tuple[int, int] = None,
    interval: float = None
):
    subject.on_next(
        ScreenshotState(
            mouse_pos=mouse_pos,
            region_size=region_size,
            interval=interval
        )
    )

def set_screenshot_state_settings(value: ScreenshotState):

    state.merge_state(value)

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
    

def init_screenshot_config_subject():
    subject.subscribe(set_screenshot_state_settings)

init_screenshot_config_subject()

if __name__ == "__main__":

   

    img = capture_screenshot_bgr()
    use_screenshot_config_subject(
        mouse_pos=(100, 200),
        region_size=(100, 100),
    )
    print(state.region)
    print(state.screen_center)