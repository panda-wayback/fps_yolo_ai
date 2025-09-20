"""
截图图片话题处理
基于PID模型的最佳实践
"""

import time
import numpy as np
from data_center.index import get_data_center
from data_center.models.screenshot.subject_model import ScreenshotSubjectModel
from utils.thread.utils import threaded


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


def init_img_subject():
    """初始化截图图片订阅"""
    # 订阅图片变化 - 使用独立线程确保并行处理
    ScreenshotSubjectModel.img_subject.subscribe(on_img_change)  # 图片保存 - 轻量级任务
    ScreenshotSubjectModel.img_subject.subscribe(detect_img)     # YOLO检测 - 重量级任务
    print("✅ 截图图片订阅初始化成功")


init_img_subject()


if __name__ == "__main__":
    # 测试用例
    import numpy as np
    
    # 模拟图片更新
    fake_img1 = np.zeros((480, 640, 3), dtype=np.uint8)
    fake_img2 = np.ones((720, 1280, 3), dtype=np.uint8) * 255
    
    ScreenshotSubjectModel.img_subject.on_next(fake_img1)
    time.sleep(0.1)
    ScreenshotSubjectModel.img_subject.on_next(fake_img2)