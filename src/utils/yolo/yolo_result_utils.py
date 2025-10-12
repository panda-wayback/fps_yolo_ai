from typing import List, Optional, Tuple
import math
from ultralytics.engine.results import Boxes, Results

def select_best_by_center_target(result: Results) -> Optional[Boxes]:
    """
    选择离图片中心最近的目标框
    
    Args:
        result: YOLO 单张图片的结果 (Results 对象)
    
    Returns:
        best_index: 最近目标的索引 (在 result.boxes 里的位置)，若无检测则返回 None
    """
    boxes = result.boxes
    if boxes is None or len(boxes) == 0:
        return None

    h, w = result.orig_shape
    center_x, center_y = w / 2, h / 2

    def distance_to_center(box):
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        bx, by = (x1 + x2) / 2, (y1 + y2) / 2
        return math.hypot(bx - center_x, by - center_y)

    distances = [distance_to_center(box) for box in boxes]
    best_index = int(min(range(len(distances)), key=lambda i: distances[i]))
    return  boxes[best_index]



def select_best_target(result: Results, selected_target_id: Optional[int] = None) -> Optional[Tuple[Tuple[float, float], Boxes]]:
    """
    选择与参考向量最相似的目标，返回中心点、边界框、置信度、类别ID

    Args:
        result: YOLO 单张图片的结果 (Results 对象)
        selected_class_ids: 选中的类别ID列表，为空时全选

    Returns:
        (selected_target_point, selected_target_bbox, selected_target_confidence, selected_target_class_id)
        如果没有检测结果，返回 None
    """
    boxes = result.boxes
    if boxes is None or len(boxes) == 0:
        return None, None, None, None
    
    h, w = result.orig_shape
    center_x, center_y = w / 2, h / 2

    def distance_to_center(box: Boxes):
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        bx, by = (x1 + x2) / 2, (y1 + y2) / 2
        return math.hypot(bx - center_x, by - center_y)
    
    def get_box_by_id(boxes: Boxes, id: int):
        ids = boxes.id.cpu().numpy().astype(int).tolist()
        if id in ids:
            idx = ids.index(id)
            return boxes[idx]
        return None
    
    # 找到最近的 box
    best_box: Boxes = get_box_by_id(boxes, selected_target_id) or min(boxes, key=distance_to_center)


    # 解析信息
    x1, y1, x2, y2 = best_box.xyxy[0].tolist()
    # 瞄准点：X轴居中，Y轴为上四分之一位置（瞄准头部）
    cx = (x1 + x2) / 2  # X轴：保持水平居中
    cy = (y1+y2) / 2 - abs(y2 - y1)/2 * 0.8 - 25  # Y轴：从顶部往下1/4处（上四分之一）
    # 计算目标瞄准点到图片中心的向量
    vector_x = cx - center_x
    vector_y = cy - center_y


    return ( (vector_x, vector_y), best_box )