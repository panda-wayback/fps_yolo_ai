#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YOLO结果处理工具函数
"""

import numpy as np
from typing import List, Dict, Any, Tuple, Optional
from utils.math.vector_utils import vector_to_polar, vector_distance, vector_similarity


def process_yolo_results(yolo_results: List[Any], screen_center: Tuple[float, float], class_ids: Optional[List[int]] = None) -> List[Dict[str, Any]]:
    """
    处理YOLO检测结果，计算向量和距离
    
    Args:
        yolo_results: YOLO检测结果列表
        screen_center: 屏幕中心点坐标 (x, y)
        class_ids: 可选的类别ID列表，只返回这些类别的目标。如果为None，返回所有类别
    
    Returns:
        处理后的目标信息列表，每个目标包含：
        - id: 目标ID
        - bbox: 边界框坐标 [x1, y1, x2, y2]
        - center: 目标中心点 [x, y]
        - vector: 从屏幕中心到目标中心的向量 [dx, dy]
        - distance: 到屏幕中心的距离
        - radius: 极坐标半径
        - angle: 极坐标角度（弧度）
        - angle_degrees: 极坐标角度（度）
        - confidence: 置信度
        - class_id: 类别ID
        - class_name: 类别名称
    """
    if not yolo_results:
        return []
    
    screen_center = np.array(screen_center)
    processed_targets = []
    
    for i, result in enumerate(yolo_results):
        # 解析YOLO结果
        if hasattr(result, 'boxes') and result.boxes is not None:
            boxes = result.boxes
            for j in range(len(boxes)):
                # 获取边界框坐标
                if hasattr(boxes.xyxy[j], 'cpu'):
                    bbox = boxes.xyxy[j].cpu().numpy()
                else:
                    bbox = boxes.xyxy[j]
                
                # 获取置信度
                if hasattr(boxes.conf[j], 'cpu'):
                    conf = float(boxes.conf[j].cpu().numpy())
                else:
                    conf = float(boxes.conf[j])
                
                # 获取类别ID
                if hasattr(boxes.cls[j], 'cpu'):
                    cls = int(boxes.cls[j].cpu().numpy())
                else:
                    cls = int(boxes.cls[j])
                
                # 如果指定了class_ids，只处理指定类别的目标
                if class_ids is not None and cls not in class_ids:
                    continue
                
                # 计算目标中心点
                target_center_x = (bbox[0] + bbox[2]) / 2
                target_center_y = (bbox[1] + bbox[3]) / 2
                target_center = np.array([target_center_x, target_center_y])
                
                # 计算从屏幕中心到目标中心的向量
                vector = target_center - screen_center
                
                # 计算距离
                distance = vector_distance(screen_center, target_center)
                
                # 计算极坐标
                radius, angle = vector_to_polar(vector)
                
                # 获取类别名称
                if hasattr(result, 'names') and cls in result.names:
                    name = result.names[cls]
                else:
                    name = f"class_{cls}"
                
                target_info = {
                    "id": f"{i}_{j}",
                    "bbox": bbox.tolist(),
                    "center": target_center.tolist(),
                    "vector": vector.tolist(),
                    "distance": float(distance),
                    "radius": float(radius),
                    "angle": float(angle),
                    "angle_degrees": float(np.degrees(angle)),
                    "confidence": conf,
                    "class_id": cls,
                    "class_name": name
                }
                
                processed_targets.append(target_info)
    
    return processed_targets




def get_targets_by_distance(targets: List[Dict[str, Any]], max_distance: float) -> List[Dict[str, Any]]:
    """
    根据距离筛选目标
    
    Args:
        targets: 目标列表
        max_distance: 最大距离
    
    Returns:
        距离小于等于max_distance的目标列表
    """
    return [target for target in targets if target['distance'] <= max_distance]


def get_targets_by_class(targets: List[Dict[str, Any]], class_ids: List[int]) -> List[Dict[str, Any]]:
    """
    根据类别筛选目标
    
    Args:
        targets: 目标列表
        class_ids: 类别ID列表
    
    Returns:
        指定类别的目标列表
    """
    if not class_ids:
        return targets
    return [target for target in targets if target['class_id'] in class_ids]


def get_closest_target(targets: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """
    获取最近的目标
    
    Args:
        targets: 目标列表
    
    Returns:
        最近的目标，如果没有目标则返回None
    """
    if not targets:
        return None
    return min(targets, key=lambda t: t['distance'])


def get_targets_by_confidence(targets: List[Dict[str, Any]], min_confidence: float) -> List[Dict[str, Any]]:
    """
    根据置信度筛选目标
    
    Args:
        targets: 目标列表
        min_confidence: 最小置信度
    
    Returns:
        置信度大于等于min_confidence的目标列表
    """
    return [target for target in targets if target['confidence'] >= min_confidence]


def sort_targets_by_distance(targets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    按距离排序目标
    
    Args:
        targets: 目标列表
    
    Returns:
        按距离从近到远排序的目标列表
    """
    return sorted(targets, key=lambda t: t['distance'])


def sort_targets_by_confidence(targets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    按置信度排序目标
    
    Args:
        targets: 目标列表
    
    Returns:
        按置信度从高到低排序的目标列表
    """
    return sorted(targets, key=lambda t: t['confidence'], reverse=True)


# 便捷函数
def process_yolo_results_simple(yolo_results: List[Any], screen_center: Tuple[float, float], class_ids: Optional[List[int]] = None) -> List[Dict[str, Any]]:
    """
    简化版YOLO结果处理函数
    只返回基本的目标信息：中心点、向量、距离、类别
    
    Args:
        yolo_results: YOLO检测结果列表
        screen_center: 屏幕中心点坐标 (x, y)
        class_ids: 可选的类别ID列表，只返回这些类别的目标。如果为None，返回所有类别
    """
    targets = process_yolo_results(yolo_results, screen_center, class_ids)
    
    # 简化输出
    simple_targets = []
    for target in targets:
        simple_target = {
            "center": target["center"],
            "vector": target["vector"],
            "distance": target["distance"],
            "class_name": target["class_name"],
            "confidence": target["confidence"]
        }
        simple_targets.append(simple_target)
    
    return simple_targets


def _calculate_target_scores(targets: List[Dict[str, Any]], 
                           reference_vector: Optional[np.ndarray] = None,
                           distance_weight: float = 0.3,
                           similarity_weight: float = 0.4,
                           confidence_weight: float = 0.3) -> List[Dict[str, Any]]:
    """
    计算目标的综合评分（内部函数）
    
    Args:
        targets: 目标列表
        reference_vector: 参考向量
        distance_weight: 距离权重
        similarity_weight: 相似度权重
        confidence_weight: 置信度权重
    
    Returns:
        添加了评分信息的目标列表
    """
    if not targets:
        return []
    
    # 确保权重和为1
    total_weight = distance_weight + similarity_weight + confidence_weight
    if total_weight > 0:
        distance_weight /= total_weight
        similarity_weight /= total_weight
        confidence_weight /= total_weight
    
    # 计算每个目标的综合评分
    for target in targets:
        # 距离评分 (距离越近评分越高)
        max_distance = max(t['distance'] for t in targets) if len(targets) > 1 else 1
        distance_score = 1.0 - (target['distance'] / max_distance) if max_distance > 0 else 1.0
        
        # 置信度评分 (置信度越高评分越高)
        confidence_score = target['confidence']
        
        # 相似度评分
        if reference_vector is not None:
            target_vector = np.array(target['vector'])
            # 避免零向量
            if np.linalg.norm(target_vector) > 0 and np.linalg.norm(reference_vector) > 0:
                similarity_score = vector_similarity(reference_vector, target_vector)
            else:
                similarity_score = 0.0
        else:
            similarity_score = 0.0
        
        # 计算综合评分
        if reference_vector is not None:
            # 有参考向量时，使用所有三个评分
            total_score = (distance_weight * distance_score + 
                          similarity_weight * similarity_score + 
                          confidence_weight * confidence_score)
        else:
            # 没有参考向量时，只使用距离和置信度
            total_score = (distance_weight * distance_score + 
                          confidence_weight * confidence_score)
        
        # 添加评分到目标信息
        target['distance_score'] = distance_score
        target['similarity_score'] = similarity_score
        target['confidence_score'] = confidence_score
        target['total_score'] = total_score
    
    return targets


def select_best_target(yolo_results: List[Any], 
                      reference_vector: Optional[np.ndarray] = None,
                      class_ids: Optional[List[int]] = None,
                      distance_weight: float = 0.3,
                      similarity_weight: float = 0.4,
                      confidence_weight: float = 0.3,
                      class_weight: float = 0.3) -> Optional[Dict[str, Any]]:
    """
    根据向量相似度、距离和置信度计算综合评分，选择最佳目标
    
    Args:
        yolo_results: YOLO检测结果列表
        screen_center: 屏幕中心点坐标 (x, y)
        reference_vector: 参考向量，用于计算相似度。如果为None，则只考虑距离和置信度
        class_ids: 可选的类别ID列表，只考虑这些类别的目标
        distance_weight: 距离权重 (0-1)
        similarity_weight: 相似度权重 (0-1)
        confidence_weight: 置信度权重 (0-1)
    
    Returns:
        评分最高的目标信息，如果没有目标则返回None
    """
    # 处理YOLO结果
    img_shape = yolo_results[0].plot().shape[:2]  # (height, width)
    screen_center = (int(img_shape[1] / 2), int(img_shape[0] / 2))  # (width/2, height/2)
    targets = process_yolo_results(yolo_results, screen_center, class_ids)
    
    if not targets:
        return None
    
    # 计算评分
    targets = _calculate_target_scores(targets, reference_vector, 
                                     distance_weight, similarity_weight, confidence_weight)
    
    # 找到最佳目标
    return max(targets, key=lambda t: t['total_score'])


def select_best_targets(yolo_results: List[Any], 
                       screen_center: Tuple[float, float], 
                       reference_vector: Optional[np.ndarray] = None,
                       class_ids: Optional[List[int]] = None,
                       distance_weight: float = 0.3,
                       similarity_weight: float = 0.4,
                       confidence_weight: float = 0.3,
                       top_k: int = 3) -> List[Dict[str, Any]]:
    """
    根据向量相似度、距离和置信度计算综合评分，返回评分最高的前k个目标
    
    Args:
        yolo_results: YOLO检测结果列表
        screen_center: 屏幕中心点坐标 (x, y)
        reference_vector: 参考向量，用于计算相似度
        class_ids: 可选的类别ID列表，只考虑这些类别的目标
        distance_weight: 距离权重 (0-1)
        similarity_weight: 相似度权重 (0-1)
        confidence_weight: 置信度权重 (0-1)
        top_k: 返回前k个目标
    
    Returns:
        按评分排序的目标列表
    """
    # 处理YOLO结果
    targets = process_yolo_results(yolo_results, screen_center, class_ids)
    
    if not targets:
        return []
    
    # 计算评分
    targets = _calculate_target_scores(targets, reference_vector, 
                                     distance_weight, similarity_weight, confidence_weight)
    
    # 按评分排序并返回前k个
    sorted_targets = sorted(targets, key=lambda t: t['total_score'], reverse=True)
    return sorted_targets[:top_k]


if __name__ == "__main__":
    # 测试YOLO结果处理工具函数
    print("=== YOLO结果处理工具函数测试 ===")
    
    # 模拟YOLO结果
    class MockYoloResult:
        def __init__(self, boxes, conf, cls, names):
            self.boxes = boxes
            self.conf = conf
            self.cls = cls
            self.names = names

    class MockBoxes:
        def __init__(self, xyxy, conf, cls):
            self.xyxy = xyxy
            self.conf = conf
            self.cls = cls
        
        def __len__(self):
            return len(self.xyxy)
        
        def __getitem__(self, index):
            return self.xyxy[index]

    # 创建模拟数据 - 包含不同类别的目标
    boxes_data = np.array([
        [100, 100, 200, 200],  # 目标1: 中心(150, 150) 类别0
        [300, 300, 400, 400],  # 目标2: 中心(350, 350) 类别1
        [150, 150, 250, 250],  # 目标3: 中心(200, 200) 类别0
        [500, 100, 600, 200],  # 目标4: 中心(550, 150) 类别2
        [200, 400, 300, 500],  # 目标5: 中心(250, 450) 类别0
    ])

    conf_data = np.array([0.8, 0.6, 0.9, 0.7, 0.85])
    cls_data = np.array([0, 1, 0, 2, 0])  # 不同类别

    boxes = MockBoxes(boxes_data, conf_data, cls_data)
    names = {0: 'enemy', 1: 'friendly', 2: 'neutral'}

    yolo_results = [MockYoloResult(boxes, conf_data, cls_data, names)]
    screen_center = (320, 240)

    print(f"屏幕中心: {screen_center}")
    print(f"检测到 {len(boxes_data)} 个目标")
    print()

    # 测试1: 基本处理
    print("--- 测试1: 基本YOLO结果处理 ---")
    all_targets = process_yolo_results(yolo_results, screen_center)
    print(f"处理结果: {len(all_targets)} 个目标")
    for target in all_targets:
        print(f"  目标 {target['id']}: {target['class_name']} "
              f"中心=({target['center'][0]:.0f}, {target['center'][1]:.0f}) "
              f"距离={target['distance']:.1f} 置信度={target['confidence']:.2f}")
    print()

    # 测试2: 类别筛选
    print("--- 测试2: 类别筛选 (只选择敌人) ---")
    enemy_targets = process_yolo_results(yolo_results, screen_center, class_ids=[0])
    print(f"敌人目标: {len(enemy_targets)} 个")
    for target in enemy_targets:
        print(f"  目标 {target['id']}: {target['class_name']} 距离={target['distance']:.1f}")
    print()

    # 测试3: 无参考向量的最佳目标选择
    print("--- 测试3: 无参考向量的最佳目标选择 ---")
    best_target = select_best_target(yolo_results, screen_center)
    if best_target:
        print(f"最佳目标: {best_target['id']} ({best_target['class_name']})")
        print(f"  中心: ({best_target['center'][0]:.0f}, {best_target['center'][1]:.0f})")
        print(f"  距离: {best_target['distance']:.1f}")
        print(f"  置信度: {best_target['confidence']:.2f}")
        print(f"  距离评分: {best_target['distance_score']:.3f}")
        print(f"  置信度评分: {best_target['confidence_score']:.3f}")
        print(f"  总评分: {best_target['total_score']:.3f}")
    print()

    # 测试4: 有参考向量的最佳目标选择
    print("--- 测试4: 有参考向量的最佳目标选择 ---")
    reference_vector = np.array([100, -50])  # 向右上方
    print(f"参考向量: {reference_vector}")
    best_target = select_best_target(yolo_results, screen_center, reference_vector)
    if best_target:
        print(f"最佳目标: {best_target['id']} ({best_target['class_name']})")
        print(f"  中心: ({best_target['center'][0]:.0f}, {best_target['center'][1]:.0f})")
        print(f"  向量: ({best_target['vector'][0]:.0f}, {best_target['vector'][1]:.0f})")
        print(f"  距离: {best_target['distance']:.1f}")
        print(f"  置信度: {best_target['confidence']:.2f}")
        print(f"  距离评分: {best_target['distance_score']:.3f}")
        print(f"  相似度评分: {best_target['similarity_score']:.3f}")
        print(f"  置信度评分: {best_target['confidence_score']:.3f}")
        print(f"  总评分: {best_target['total_score']:.3f}")
    print()

    # 测试5: 前3个目标
    print("--- 测试5: 前3个最佳目标 ---")
    top_targets = select_best_targets(yolo_results, screen_center, reference_vector, top_k=3)
    print("前3个目标:")
    for i, target in enumerate(top_targets):
        print(f"  {i+1}. 目标{target['id']} ({target['class_name']}): "
              f"总评分={target['total_score']:.3f} 距离={target['distance']:.1f}")
    print()

    # 测试6: 自定义权重
    print("--- 测试6: 自定义权重 (重视相似度) ---")
    best_target = select_best_target(yolo_results, screen_center, reference_vector,
                                   distance_weight=0.2, similarity_weight=0.6, confidence_weight=0.2)
    if best_target:
        print(f"最佳目标 (重视相似度): {best_target['id']} 总评分={best_target['total_score']:.3f}")
    print()

    # 测试7: 不同参考向量
    print("--- 测试7: 不同参考向量 ---")
    reference_vector2 = np.array([-100, 100])  # 向左下方
    print(f"参考向量2: {reference_vector2}")
    best_target2 = select_best_target(yolo_results, screen_center, reference_vector2)
    if best_target2:
        print(f"最佳目标 (左下参考): {best_target2['id']} 总评分={best_target2['total_score']:.3f}")
    print()

    # 测试8: 简化版处理
    print("--- 测试8: 简化版处理 ---")
    simple_targets = process_yolo_results_simple(yolo_results, screen_center, class_ids=[0])
    print(f"简化版敌人目标: {len(simple_targets)} 个")
    for target in simple_targets:
        print(f"  {target['class_name']}: 中心={target['center']} 距离={target['distance']:.1f}")

    print("\n✅ 所有测试完成！")

