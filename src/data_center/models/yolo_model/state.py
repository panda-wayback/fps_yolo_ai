

from data_center.index import get_data_center


class YoloModelState:
    """YOLO模型状态类"""

    @staticmethod
    def get_state():
        """获取YOLO模型状态"""
        return get_data_center().state.yolo_model_state

    @staticmethod
    def init_subscribes():
        """初始化YOLO模型订阅"""
        from data_center.models.yolo_model.subscribes.result_subject import send_result_to_target_selector
        YoloModelState.get_state().yolo_results.subscribe(send_result_to_target_selector)
    

YoloModelState.init_subscribes()