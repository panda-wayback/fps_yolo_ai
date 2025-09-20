from rx.subject import Subject
from data_center.index import get_data_center
from data_center.models.target_selector.state import TargetSelectorState
from typing import Optional, Tuple

subject = Subject()

def use_target_selector_config_subject(
    distance_weight: Optional[float] = None,
    confidence_weight: Optional[float] = None,
    similarity_weight: Optional[float] = None,
    class_weight: Optional[float] = None,
    reference_vector: Optional[Tuple[float, float]] = None
):
    """使用目标选择器配置"""
    # 只传递非None的值
    config_data = {}
    if distance_weight is not None:
        config_data['distance_weight'] = distance_weight
    if confidence_weight is not None:
        config_data['confidence_weight'] = confidence_weight
    if similarity_weight is not None:
        config_data['similarity_weight'] = similarity_weight
    if class_weight is not None:
        config_data['class_weight'] = class_weight
    if reference_vector is not None:
        config_data['reference_vector'] = reference_vector
    
    config = TargetSelectorState(**config_data)
    subject.on_next(config)

def set_target_selector_config(config: TargetSelectorState):
    """设置目标选择器配置"""
    state = get_data_center().state.target_selector_state
    state.merge_state(config)
    print(f"目标选择器配置已更新: distance_weight={config.distance_weight}, "
          f"confidence_weight={config.confidence_weight}, "
          f"similarity_weight={config.similarity_weight}, "
          f"class_weight={config.class_weight}")

def init_target_selector_config_subject():
    """初始化目标选择器配置订阅"""
    subject.subscribe(set_target_selector_config)

init_target_selector_config_subject()

if __name__ == "__main__":
    # 测试配置更新
    use_target_selector_config_subject(
        distance_weight=0.3,
        confidence_weight=0.4,
        similarity_weight=0.2,
        class_weight=0.1
    )
