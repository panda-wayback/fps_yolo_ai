

def listen_keyboard_click(value):
    print(f"键盘按键: {value}")
    
    from data_center.models.input_monitor.state import InputMonitorState
    if value == "o":
        from singleton_classes.simulation_move_mouse.simulation_move_mouse import get_mouse_simulator
        InputMonitorState.get_state().is_submit_vector.set(True)
        get_mouse_simulator().run()
        pass 
    elif value == "p":
        InputMonitorState.get_state().is_submit_vector.set(False)
        pass
    pass

def listen_mouse_click(value):
    #print(f"鼠标点击: {value}")
    pass





