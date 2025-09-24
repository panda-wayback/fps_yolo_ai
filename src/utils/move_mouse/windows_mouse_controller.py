from utils.move_mouse.windows_mouse_api import relative_move_sendinput


class WindowsMouseController:
    def __init__(self):
        pass
    
    def move(self, dx: int, dy: int):
        relative_move_sendinput(dx, dy)
