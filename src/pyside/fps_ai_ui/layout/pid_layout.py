from PySide6.QtWidgets import QLabel, QHBoxLayout, QWidget
from pyside.UI.basic.basic_layout import get_horizontal_layout


def get_pid_component():
    """创建PID布局组件 - 返回组件而不是布局"""
    # 创建容器组件
    widget = QWidget()
    
    # 创建布局
    layout = get_horizontal_layout()
    
    # 添加组件到布局
    layout.addWidget(QLabel("PID1"))
    layout.addWidget(QLabel("PID2"))
    layout.addWidget(QLabel("PID3"))
    
    # 将布局应用到组件
    widget.setLayout(layout)
    
    return widget