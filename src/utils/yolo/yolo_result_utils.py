from typing import List, Optional, Tuple
import math
from ultralytics.engine.results import Boxes, Results

from utils.math.vector_utils import vector_angle_between_degrees  # YOLO 的返回类型

def select_best_target_bf(result: Results) -> Optional[Boxes]:
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



def select_best_target(result: Results, reference_vector: Tuple[float, float], selected_class_ids: Optional[List[int]] = None) -> Optional[Tuple[Tuple[float, float], Tuple[float, float, float, float], float, int]]:
    """
    选择与参考向量最相似的目标，返回中心点、边界框、置信度、类别ID

    Args:
        result: YOLO 单张图片的结果 (Results 对象)
        reference_vector: 参考向量 (x, y)
        selected_class_ids: 选中的类别ID列表，为空时全选
        vector_similarity_coeff: 向量相似度系数

    Returns:
        (selected_target_point, selected_target_bbox, selected_target_confidence, selected_target_class_id)
        如果没有检测结果，返回 None
    """
    boxes = result.boxes
    if boxes is None or len(boxes) == 0:
        return None, None, None, None

    # 过滤类别
    if selected_class_ids:
        boxes = [box for box in boxes if int(box.cls.item()) in selected_class_ids]
        if not boxes:
            return None, None, None, None

    h, w = result.orig_shape
    center_x, center_y = w / 2, h / 2

    def vector_similarity(box: Boxes):
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        bx, by = (x1 + x2) / 2, (y1 + y2) / 2
        target_vector = (bx - center_x, by - center_y)
        
        # 计算距离相似度（归一化到0-1）
        max_distance = math.hypot(w/2, h/2)  # 图片对角线长度作为最大距离
        distance_similarity = math.hypot(target_vector[0] - reference_vector[0], target_vector[1] - reference_vector[1]) #/ max_distance * 2
        
        # 计算角度相似度（已经归一化到0-1）
        angle_similarity = vector_angle_between_degrees(target_vector, reference_vector) / 180
        # 返回归一化后的最小值
        return distance_similarity + angle_similarity
        
    # 找到最相似的目标
    best_box: Boxes = min(boxes, key=vector_similarity)

    # 解析信息
    x1, y1, x2, y2 = best_box.xyxy[0].tolist()
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    vector_x = cx - center_x
    vector_y = cy - center_y
    conf = float(best_box.conf.item())
    cls_id = int(best_box.cls.item())

    return ( (vector_x, vector_y), (x1, y1, x2, y2), conf, cls_id )
