#!/usr/bin/env python3
"""
统一订阅接口使用示例
"""

from src.data_center.subjects import subjects
import numpy as np

def main():
    """演示统一订阅接口的使用"""
    print("=== 统一订阅接口使用示例 ===")
    
    # 1. 截图配置
    print("\n1. 配置截图参数...")
    subjects.screenshot.use_config(
        mouse_pos=(960, 540),  # 屏幕中心
        region_size=(200, 200),  # 截图区域大小
        interval=0.1  # 截图间隔
    )
    
    # 2. YOLO模型配置
    print("\n2. 加载YOLO模型...")
    subjects.yolo.use_model("path/to/your/model.pt")
    
    # 3. PID参数配置
    print("\n3. 配置PID参数...")
    subjects.pid.use_config(kp=1.5, ki=0.1, kd=0.05)
    
    # 4. 发送图片进行检测
    print("\n4. 发送图片进行检测...")
    fake_img = np.zeros((480, 640, 3), dtype=np.uint8)
    subjects.screenshot.send_image(fake_img)
    
    # 5. 获取各种订阅
    print("\n5. 获取订阅对象...")
    img_subject = subjects.screenshot.get_img_subject()
    yolo_detect_subject = subjects.yolo.get_detect_subject()
    pid_config_subject = subjects.pid.get_config_subject()
    
    print("✅ 所有配置完成！")
    print(f"图片订阅: {img_subject}")
    print(f"YOLO检测订阅: {yolo_detect_subject}")
    print(f"PID配置订阅: {pid_config_subject}")

if __name__ == "__main__":
    main()
