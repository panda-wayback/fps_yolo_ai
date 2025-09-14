from PySide6.QtWidgets import QGroupBox, QLabel, QHBoxLayout, QWidget
from pyside.UI.basic.basic_layout import create_horizontal_card, create_vertical_card, get_horizontal_layout
from pyside.fps_ai_ui.component.pid_component.component.pid_parameters import get_pid_control_widget





def get_pid_component():
    card: QGroupBox = create_horizontal_card("PID 参数控制")
    """创建PID布局组件 - 返回组件而不是布局"""
    layout: QHBoxLayout = card._layout
    # 添加组件到布局
    layout.addWidget(QLabel("PID1"))
    layout.addWidget(get_pid_control_widget())
    return card