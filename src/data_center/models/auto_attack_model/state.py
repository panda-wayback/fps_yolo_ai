from data_center.index import get_data_center
from data_center.models.auto_attack_model.model import AutoAttackModel
from utils.thread.main import threaded


class AutoAttackModelState:
    """自动攻击模型状态管理类"""
    @staticmethod
    def get_state() -> AutoAttackModel:
        """获取状态"""
        return get_data_center().state.auto_attack_model_state

    @staticmethod
    def init_subscribes():
        from data_center.models.auto_attack_model.subscribes.auto_attack import auto_track, auto_attack
        AutoAttackModelState.get_state().track_point.subscribe(threaded(auto_track))
        AutoAttackModelState.get_state().track_point.subscribe(threaded(auto_attack))

        pass
