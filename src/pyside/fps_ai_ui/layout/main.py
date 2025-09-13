from PySide6.QtWidgets import QLabel, QWidget
from pyside.basic.basic_layout import get_vertical_layout




def pid_layout():
    layout = get_vertical_layout()
    layout.addWidget(QLabel("PID"))
    return layout



def set_main_layout(window: QWidget):
    layout = get_vertical_layout()
    layout.addLayout(pid_layout())


    layout.addWidget(window)
    return layout