def init_state():
    from data_center.models.input_monitor.state import InputMonitorState
    from data_center.models.screenshot.state import ScreenshotModelState
    from data_center.models.yolo_model.state import YoloModelState
    from data_center.models.mouse_driver_model.state import MouseDriverState
    from data_center.models.controller_model.state import ControllerModelState
    from data_center.models.target_selector.state import TargetSelectorState
    InputMonitorState.init_subscribes()
    ScreenshotModelState.init_subscribes()
    YoloModelState.init_subscribes()
    MouseDriverState.init_subscribes()
    ControllerModelState.init_subscribes()
    TargetSelectorState.init_subscribes()
    
    pass

if __name__ == "__main__":
    init_state()