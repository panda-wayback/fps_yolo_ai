from data_center.index import get_data_center



class InputMonitorState:
    """输入监控器状态"""
    @staticmethod
    def get_state():
        return get_data_center().state.input_monitor_state

    @staticmethod
    def init_subscribes():
        from data_center.models.input_monitor.utils.input_utils import listen_keyboard_click
        InputMonitorState.get_state().keyboard_click_name.subscribe(
            listen_keyboard_click
        )
        pass


