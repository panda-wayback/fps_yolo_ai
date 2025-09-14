

import sys
from PySide6.QtWidgets import QApplication, QGroupBox, QWidget

from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout
from pyside.UI.basic.basic_layout import create_card, create_vertical_card, get_vertical_layout
from pyside.UI.basic.basic_window import create_basic_window
from pyside.fps_ai_ui.component.pid_component.index import get_pid_component
from pyside.fps_ai_ui.component.yolo_model.index import get_yolo_model_component



# PID参数控制组件
def pid_component() -> QGroupBox:
    return get_pid_component()

# YOLO模型选择组件
def yolo_model_component() -> QGroupBox:
    return get_yolo_model_component()

# 主布局
def get_main_layout():
    # 设置垂直布局
    layout = get_vertical_layout()

    # 获取组件
    # YOLO模型选择组件
    layout.addWidget(yolo_model_component())
    # PID参数控制组件
    layout.addWidget(pid_component())
    

    return layout


def prompt_window(window: QWidget):
    """将窗口移动到指定屏幕"""
    app = QApplication.instance()  # 获取现有的 QApplication 实例
    screens = app.screens()
    if len(screens) > 1:
        screen = screens[1]  # 使用第二个屏幕
        window.move(screen.geometry().x(), screen.geometry().y())
    window.show()



def main_window():
    app = QApplication(sys.argv)
    window = create_basic_window()

    window.setLayout(get_main_layout())

    prompt_window(window)
    sys.exit(app.exec())


if __name__ == "__main__":
    main_window()