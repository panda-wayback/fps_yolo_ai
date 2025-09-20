from typing import Optional, Tuple
from pydantic import ConfigDict
from data_center.models.base_state import BaseState


class TargetSelectorState(BaseState):
    """目标选择器状态"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    # 目标信息
    selected_point: Optional[Tuple[float, float]] = None  # 选中目标的中心点 (x, y)
    selected_bbox: Optional[Tuple[float, float, float, float]] = None  # 选中目标的边界框 (x1, y1, x2, y2)
    selected_confidence: Optional[float] = None  # 选中目标的置信度
    selected_class_id: Optional[int] = None  # 选中目标的类别ID
    
    # 配置参数
    distance_weight: float = 0.5  # 距离权重
    confidence_weight: float = 0.5  # 置信度权重
    similarity_weight: float = 0.5  # 相似度权重
    # 类别权重
    class_weight: float = 0.5  # 类别权重
    # 参考向量
    reference_vector: Optional[Tuple[float, float]] = None  # 参考向量
    
