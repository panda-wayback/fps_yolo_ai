from data_center.index import get_data_center



class InputMonitorState:
    """输入监控器状态"""
    @staticmethod
    def get_state():
        return get_data_center().state.input_monitor_state

    @staticmethod
    def init_subscribes():
        from data_center.models.input_monitor.utils.input_utils import listen_keyboard_to_start_screenshot
        InputMonitorState.get_state().keyboard_click_name.subscribe(
            listen_keyboard_to_start_screenshot
        )
        from data_center.models.input_monitor.utils.input_utils import listen_keyboard_to_start_screenshot
        InputMonitorState.get_state().mouse_left_click_time.subscribe(
            listen_keyboard_to_start_screenshot
        )
        pass


