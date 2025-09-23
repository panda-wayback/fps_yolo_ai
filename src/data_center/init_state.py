def init_state():
    from data_center.models.input_monitor.state import InputMonitorState
    from data_center.models.screenshot.state import ScreenshotModelState
    from data_center.models.yolo_model.state import YoloModelState
    from data_center.models.mouse_driver_model.state import MouseDriverState
    from data_center.models.pid_model.state import PIDModelState
    InputMonitorState.init_subscribes()
    ScreenshotModelState.init_subscribes()
    YoloModelState.init_subscribes()
    MouseDriverState.init_subscribes()
    PIDModelState.init_subscribes()
    pass

if __name__ == "__main__":
    init_state()