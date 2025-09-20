"""
截图图片话题处理
基于PID模型的最佳实践
"""

import time
import numpy as np
from data_center.index import get_data_center


def get_state():
    """获取截图状态"""
    return get_data_center().state.screenshot_state


def on_img_change(img: np.ndarray):
    """图片变化时的回调函数"""
    try:
        if img is not None:
            state = get_state()
            state.screenshot_img = img
            print(f"✅ 截图图片已更新: shape={img.shape}")
        else:
            print("⚠️ 图片被清空")
    except Exception as e:
        print(f"❌ 图片更新失败: {e}")


def detect_img(img: np.ndarray):
    """检测图片 - 发送到YOLO模型"""
    try:
        from data_center.models.yolo_model.subject import YoloSubject
        YoloSubject.send_detect(img)
        print(f"✅ 图片已发送到YOLO检测: shape={img.shape}")
    except Exception as e:
        print(f"❌ YOLO检测发送失败: {e}")



if __name__ == "__main__":
    # 测试用例
    import numpy as np
    
    # 模拟图片更新
    fake_img1 = np.zeros((480, 640, 3), dtype=np.uint8)
    fake_img2 = np.ones((720, 1280, 3), dtype=np.uint8) * 255
