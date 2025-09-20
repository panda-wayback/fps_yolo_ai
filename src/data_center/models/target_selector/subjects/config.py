"""
目标选择器配置话题处理
基于PID模型的最佳实践
"""

from data_center.index import get_data_center
from data_center.models.target_selector.state_model import TargetSelectorState
from data_center.models.target_selector.subject_model import TargetSelectorSubjectModel


def set_target_selector_config(config: TargetSelectorState):
    """设置目标选择器配置"""
    try:
        state = get_data_center().state.target_selector_state
        state.merge_state(config)
        print(f"✅ 目标选择器配置已更新: distance_weight={config.distance_weight}, "
              f"confidence_weight={config.confidence_weight}, "
              f"similarity_weight={config.similarity_weight}, "
              f"class_weight={config.class_weight}")
    except Exception as e:
        print(f"❌ 目标选择器配置更新失败: {e}")


def init_config_subject():
    """初始化目标选择器配置订阅"""
    TargetSelectorSubjectModel.config_subject.subscribe(set_target_selector_config)


init_config_subject()


if __name__ == "__main__":
    # 测试用例
    config = TargetSelectorState(
        distance_weight=0.3,
        confidence_weight=0.4,
        similarity_weight=0.2,
        class_weight=0.1
    )
    TargetSelectorSubjectModel.config_subject.on_next(config)