"""
YOLO识别单例使用示例
展示如何使用YoloRecog类进行目标检测
"""

import sys
import os
import numpy as np
import cv2

# 添加src目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from yolo_recog import get_yolo_recog, load_aimlabs_model


def example_basic_usage():
    """基本使用示例"""
    print("=== 基本使用示例 ===")
    
    # 1. 获取YOLO识别单例
    yolo = get_yolo_recog()
    
    # 2. 加载模型
    if not load_aimlabs_model():
        print("❌ 模型加载失败，退出示例")
        return
    
    # 3. 检查模型状态
    print(f"模型信息: {yolo.get_model_info()}")
    
    # 4. 模拟一张测试图像（实际使用时替换为真实图像）
    test_image = np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8)
    
    # 5. 进行目标检测
    detections = yolo.detect(test_image, conf_threshold=0.5)
    print(f"检测到 {len(detections)} 个目标")
    
    # 6. 打印检测结果
    for i, detection in enumerate(detections):
        print(f"目标 {i+1}:")
        print(f"  类别: {detection['name']} (ID: {detection['cls']})")
        print(f"  置信度: {detection['conf']:.3f}")
        print(f"  边界框: {detection['bbox']}")


def example_with_center_points():
    """带中心点坐标的检测示例"""
    print("\n=== 带中心点坐标的检测示例 ===")
    
    yolo = get_yolo_recog()
    
    if not yolo.is_loaded():
        print("❌ 模型未加载")
        return
    
    # 模拟测试图像
    test_image = np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8)
    
    # 检测并获取中心点
    detections = yolo.detect_center(test_image, conf_threshold=0.3)
    
    print(f"检测到 {len(detections)} 个目标（包含中心点）")
    
    for i, detection in enumerate(detections):
        print(f"目标 {i+1}:")
        print(f"  类别: {detection['name']}")
        print(f"  置信度: {detection['conf']:.3f}")
        print(f"  中心点: ({detection['center'][0]:.1f}, {detection['center'][1]:.1f})")
        print(f"  边界框: {detection['bbox']}")


def example_with_real_image():
    """使用真实图像的示例（需要提供图像文件）"""
    print("\n=== 真实图像检测示例 ===")
    
    yolo = get_yolo_recog()
    
    if not yolo.is_loaded():
        print("❌ 模型未加载")
        return
    
    # 这里可以加载真实的图像文件
    # image_path = "path/to/your/image.jpg"
    # if os.path.exists(image_path):
    #     image = cv2.imread(image_path)
    #     image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    #     
    #     detections = yolo.detect_center(image)
    #     print(f"在真实图像中检测到 {len(detections)} 个目标")
    #     
    #     for detection in detections:
    #         print(f"检测到: {detection['name']} (置信度: {detection['conf']:.3f})")
    # else:
    #     print("图像文件不存在，跳过真实图像示例")
    
    print("真实图像示例需要提供图像文件路径")


def example_multiple_instances():
    """多实例测试（验证单例模式）"""
    print("\n=== 单例模式验证 ===")
    
    # 创建多个实例
    yolo1 = get_yolo_recog()
    yolo2 = get_yolo_recog()
    yolo3 = YoloRecog()
    
    # 验证是否为同一个实例
    print(f"yolo1 id: {id(yolo1)}")
    print(f"yolo2 id: {id(yolo2)}")
    print(f"yolo3 id: {id(yolo3)}")
    print(f"是否为同一实例: {yolo1 is yolo2 is yolo3}")
    
    # 验证模型状态共享
    if yolo1.is_loaded():
        print("✅ 所有实例共享同一个模型状态")
    else:
        print("❌ 模型未加载")


if __name__ == "__main__":
    # 运行所有示例
    example_basic_usage()
    example_with_center_points()
    example_with_real_image()
    example_multiple_instances()
    
    print("\n=== 示例完成 ===")
    print("你可以根据需要修改和扩展这些示例")
