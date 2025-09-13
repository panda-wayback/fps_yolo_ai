"""
FPS游戏AI辅助主程序 - 最小示例
加载YOLO模型并检测鼠标周围的目标，显示截图和检测结果
"""

import cv2


def draw_detections(image, boxes, classes, confidences):
    """
    在图像上绘制检测结果
    
    参数:
        image: 原始图像
        boxes: 边界框坐标 (x1, y1, x2, y2)
        classes: 类别索引
        confidences: 置信度
    
    返回:
        绘制了检测结果的图像
    """
    # 复制图像以避免修改原始图像
    result_image = image.copy()
    
    # 定义颜色 (BGR格式)
    colors = [
        (0, 255, 0),    # 绿色
        (255, 0, 0),    # 蓝色
        (0, 0, 255),    # 红色
        (255, 255, 0),  # 青色
        (255, 0, 255),  # 洋红色
        (0, 255, 255),  # 黄色
    ]
    
    # 绘制每个检测框
    for i, box in enumerate(boxes):
        x1, y1, x2, y2 = box.tolist()
        cls = int(classes[i])
        conf = float(confidences[i])
        
        # 选择颜色
        color = colors[cls % len(colors)]
        
        # 绘制边界框
        cv2.rectangle(result_image, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
        
        # 绘制标签和置信度
        label = f"Class {cls}: {conf:.2f}"
        label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
        
        # 绘制标签背景
        cv2.rectangle(result_image, 
                     (int(x1), int(y1) - label_size[1] - 10), 
                     (int(x1) + label_size[0], int(y1)), 
                     color, -1)
        
        # 绘制标签文字
        cv2.putText(result_image, label, 
                   (int(x1), int(y1) - 5), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    
    return result_image


def show_image(image, results):
    # 处理检测结果
    res = results[0]  # 单张图像
    boxes = res.boxes.xyxy  # 边界框 (x1, y1, x2, y2)
    classes = res.boxes.cls  # 类别索引
    confidences = res.boxes.conf  # 置信度
    
    # 在图像上绘制检测结果
    result_image = draw_detections(image, boxes, classes, confidences)
    
    # 显示结果
    cv2.imshow('FPS AI - 实时检测', result_image)
