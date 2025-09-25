"""
FPS游戏AI辅助主程序 - 最小示例
加载YOLO模型并检测鼠标周围的目标，显示截图和检测结果
"""

import time
import cv2

from singleton_classes.simulation_move_mouse.simulation_move_mouse import get_mouse_simulator

def init_state():
    from data_center.init_state import init_state
    init_state()
    pass


def load_yolo_model():
    from data_center.models.yolo_model.subject import YoloSubject
    YoloSubject.send_model_path("aimlabs.pt")
    pass

def load_screenshot():
    from singleton_classes.screenshot_img.main import get_screenshot
    screenshot = get_screenshot()
    screenshot.start()
    # get_mouse_simulator().run()
    pass

def img_show():
    """显示YOLO标记的图片"""
    from utils.image_converter import get_displayable_marked_img
    
    while True:
        try:
            # 获取可显示的标记图片
            displayable_img = get_displayable_marked_img(target_format="opencv")
            
            if displayable_img is not None:
                cv2.imshow('FPS AI - 实时检测', displayable_img)
                # print("✅ 图片显示成功")
            else:
                print("⚠️ 没有可显示的图片")
            
        except Exception as e:
            print(f"❌ 图片显示错误: {e}")

        # 检查是否按下了 'q' 键退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
        time.sleep(0.01)

def main():
    init_state()
    load_yolo_model()
    load_screenshot()
    img_show()

    pass


if __name__ == "__main__":
    main()
    time.sleep(100)