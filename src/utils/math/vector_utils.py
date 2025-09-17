#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
向量数学工具函数 - 优化版
使用math标准库和numpy库提供高效的向量数学运算
"""

import numpy as np
import math
from typing import Union, Tuple, List


def vector_to_polar(vector: Union[np.ndarray, List[float], Tuple[float, float]]) -> Tuple[float, float]:
    """
    将向量转换为极坐标 - 优化版
    
    Args:
        vector: 输入向量，支持numpy数组、列表或元组
               支持2D向量 [x, y] 或 [x, y, z] (z分量会被忽略)
    
    Returns:
        Tuple[float, float]: (半径, 角度)
                            - 半径: 向量的模长
                            - 角度: 弧度制，范围 [-π, π]
    
    Examples:
        >>> vector_to_polar([3, 4])
        (5.0, 0.9272952180016122)  # 半径5，角度约53.13度
        
        >>> vector_to_polar([1, 1])
        (1.4142135623730951, 0.7853981633974483)  # 半径√2，角度45度
    """
    # 快速转换为numpy数组
    if isinstance(vector, (list, tuple)):
        vector = np.array(vector, dtype=np.float64)
    elif not isinstance(vector, np.ndarray):
        vector = np.array(vector, dtype=np.float64)
    
    # 输入验证和预处理
    if vector.ndim == 0:
        raise ValueError("向量不能是标量")
    if vector.ndim > 1:
        raise ValueError("向量必须是一维数组")
    if len(vector) < 2:
        raise ValueError("向量至少需要2个分量")
    
    # 只取前两个分量（处理3D向量）
    x, y = vector[0], vector[1]
    
    # 使用numpy的高效函数计算
    radius = np.sqrt(x*x + y*y)  # 比np.linalg.norm更快
    
    # 使用math.atan2获得更好的精度
    angle = math.atan2(y, x)
    
    return float(radius), float(angle)


def polar_to_vector(radius: float, angle: float) -> np.ndarray:
    """
    将极坐标转换为向量 - 优化版
    
    Args:
        radius: 半径（模长）
        angle: 角度（弧度制）
    
    Returns:
        np.ndarray: 2D向量 [x, y]
    
    Examples:
        >>> polar_to_vector(5.0, math.pi/4)
        array([3.53553391, 3.53553391])
    """
    # 使用numpy的三角函数，支持向量化操作
    cos_val = np.cos(angle)
    sin_val = np.sin(angle)
    
    return np.array([radius * cos_val, radius * sin_val], dtype=np.float64)


def vector_to_polar_degrees(vector: Union[np.ndarray, List[float], Tuple[float, float]]) -> Tuple[float, float]:
    """
    将向量转换为极坐标（角度制） - 优化版
    
    Args:
        vector: 输入向量
    
    Returns:
        Tuple[float, float]: (半径, 角度)
                            - 半径: 向量的模长
                            - 角度: 角度制，范围 [-180°, 180°]
    """
    radius, angle_rad = vector_to_polar(vector)
    # 使用numpy的degrees函数，支持向量化
    angle_deg = np.degrees(angle_rad)
    
    return radius, float(angle_deg)


def polar_degrees_to_vector(radius: float, angle_deg: float) -> np.ndarray:
    """
    将极坐标（角度制）转换为向量 - 优化版
    
    Args:
        radius: 半径
        angle_deg: 角度（角度制）
    
    Returns:
        np.ndarray: 2D向量 [x, y]
    """
    # 使用numpy的radians函数
    angle_rad = np.radians(angle_deg)
    return polar_to_vector(radius, angle_rad)


def normalize_vector(vector: Union[np.ndarray, List[float], Tuple[float, float]]) -> np.ndarray:
    """
    向量归一化（单位化） - 优化版
    
    Args:
        vector: 输入向量
    
    Returns:
        np.ndarray: 归一化后的向量
    
    Examples:
        >>> normalize_vector([3, 4])
        array([0.6, 0.8])
    """
    # 快速转换为numpy数组
    if not isinstance(vector, np.ndarray):
        vector = np.array(vector, dtype=np.float64)
    
    # 使用numpy的高效范数计算
    norm = np.linalg.norm(vector)
    
    # 避免除零，使用numpy的where函数
    if norm == 0:
        return np.zeros_like(vector)
    
    return vector / norm


def vector_angle_between(v1: Union[np.ndarray, List[float]], 
                        v2: Union[np.ndarray, List[float]]) -> float:
    """
    计算两个向量之间的夹角（弧度） - 优化版
    
    Args:
        v1: 第一个向量
        v2: 第二个向量
    
    Returns:
        float: 夹角（弧度），范围 [0, π]
    
    Examples:
        >>> vector_angle_between([1, 0], [0, 1])
        1.5707963267948966  # 90度
    """
    # 快速转换为numpy数组
    v1 = np.asarray(v1, dtype=np.float64)
    v2 = np.asarray(v2, dtype=np.float64)
    
    # 使用numpy的高效点积和范数计算
    dot_product = np.dot(v1, v2)
    norm_product = np.linalg.norm(v1) * np.linalg.norm(v2)
    
    # 避免除零
    if norm_product == 0:
        return 0.0
    
    # 计算余弦值并处理数值误差
    cos_angle = np.clip(dot_product / norm_product, -1.0, 1.0)
    
    # 使用numpy的arccos函数
    return float(np.arccos(cos_angle))


def vector_angle_between_degrees(v1: Union[np.ndarray, List[float]], 
                                v2: Union[np.ndarray, List[float]]) -> float:
    """
    计算两个向量之间的夹角（角度制） - 优化版
    
    Args:
        v1: 第一个向量
        v2: 第二个向量
    
    Returns:
        float: 夹角（角度），范围 [0°, 180°]
    """
    angle_rad = vector_angle_between(v1, v2)
    # 使用numpy的degrees函数
    return float(np.degrees(angle_rad))


def vector_similarity(v1: Union[np.ndarray, List[float]], 
                     v2: Union[np.ndarray, List[float]]) -> float:
    """
    计算两个向量的相似度（余弦相似度） - 优化版
    
    Args:
        v1: 第一个向量
        v2: 第二个向量
    
    Returns:
        float: 相似度，范围 [-1, 1]
               1表示完全相同方向，-1表示完全相反方向，0表示垂直
    """
    # 快速转换为numpy数组
    v1 = np.asarray(v1, dtype=np.float64)
    v2 = np.asarray(v2, dtype=np.float64)
    
    # 使用numpy的高效范数计算
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)
    
    # 避免除零
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    # 使用numpy的高效点积计算
    return float(np.dot(v1, v2) / (norm1 * norm2))


def batch_vector_to_polar(vectors: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    批量将向量转换为极坐标 - 高性能版本
    
    Args:
        vectors: 形状为 (n, 2) 的向量数组
    
    Returns:
        Tuple[np.ndarray, np.ndarray]: (半径数组, 角度数组)
    """
    if vectors.shape[1] != 2:
        raise ValueError("向量数组必须是 (n, 2) 形状")
    
    x, y = vectors[:, 0], vectors[:, 1]
    radius = np.sqrt(x*x + y*y)
    angle = np.arctan2(y, x)
    
    return radius, angle


def batch_vector_similarity(vectors1: np.ndarray, vectors2: np.ndarray) -> np.ndarray:
    """
    批量计算向量相似度 - 高性能版本
    
    Args:
        vectors1: 形状为 (n, 2) 的向量数组
        vectors2: 形状为 (n, 2) 的向量数组
    
    Returns:
        np.ndarray: 相似度数组
    """
    if vectors1.shape != vectors2.shape:
        raise ValueError("两个向量数组形状必须相同")
    
    # 计算点积
    dot_products = np.sum(vectors1 * vectors2, axis=1)
    
    # 计算范数
    norms1 = np.linalg.norm(vectors1, axis=1)
    norms2 = np.linalg.norm(vectors2, axis=1)
    
    # 避免除零
    norm_products = norms1 * norms2
    norm_products = np.where(norm_products == 0, 1, norm_products)
    
    return dot_products / norm_products


def vector_distance(v1: Union[np.ndarray, List[float]], 
                   v2: Union[np.ndarray, List[float]]) -> float:
    """
    计算两个向量之间的欧几里得距离 - 优化版
    
    Args:
        v1: 第一个向量
        v2: 第二个向量
    
    Returns:
        float: 欧几里得距离
    """
    v1 = np.asarray(v1, dtype=np.float64)
    v2 = np.asarray(v2, dtype=np.float64)
    
    return float(np.linalg.norm(v1 - v2))


def vector_rotate(vector: Union[np.ndarray, List[float]], 
                 angle: float) -> np.ndarray:
    """
    将向量旋转指定角度 - 优化版
    
    Args:
        vector: 输入向量
        angle: 旋转角度（弧度）
    
    Returns:
        np.ndarray: 旋转后的向量
    """
    vector = np.asarray(vector, dtype=np.float64)
    
    # 旋转矩阵
    cos_a, sin_a = np.cos(angle), np.sin(angle)
    rotation_matrix = np.array([[cos_a, -sin_a], [sin_a, cos_a]])
    
    return np.dot(rotation_matrix, vector)


if __name__ == "__main__":
    # 测试代码
    print("=== 向量数学工具测试 ===")
    
    # 测试向量转极坐标
    test_vectors = [
        [3, 4],
        [1, 1],
        [-1, 0],
        [0, 1],
        [-1, -1]
    ]
    
    print("\n1. 向量转极坐标测试:")
    for vec in test_vectors:
        radius, angle_rad = vector_to_polar(vec)
        radius_deg, angle_deg = vector_to_polar_degrees(vec)
        print(f"向量 {vec} -> 极坐标: 半径={radius:.2f}, 角度={angle_rad:.2f}弧度 ({angle_deg:.1f}度)")
    
    # 测试极坐标转向量
    print("\n2. 极坐标转向量测试:")
    test_polars = [
        (5.0, math.pi/4),  # 45度
        (1.0, 0),          # 0度
        (2.0, math.pi),    # 180度
        (1.0, -math.pi/2)  # -90度
    ]
    
    for radius, angle in test_polars:
        vec = polar_to_vector(radius, angle)
        print(f"极坐标 ({radius}, {angle:.2f}弧度) -> 向量: {vec}")
    
    # 测试向量相似度
    print("\n3. 向量相似度测试:")
    v1 = np.array([1, 0])
    test_v2 = [
        [1, 0],    # 相同方向
        [0, 1],    # 垂直
        [-1, 0],   # 相反方向
        [1, 1],    # 45度角
    ]
    
    for v2 in test_v2:
        similarity = vector_similarity(v1, v2)
        angle = vector_angle_between_degrees(v1, v2)
        print(f"向量 {v1} 与 {v2} 相似度: {similarity:.3f}, 夹角: {angle:.1f}度")
