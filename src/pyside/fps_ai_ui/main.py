

import sys
from PySide6.QtWidgets import QApplication, QWidget

from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout
from pyside.UI.basic.basic_layout import create_card, create_vertical_card, get_vertical_layout
from pyside.UI.basic.basic_window import create_basic_window
from pyside.fps_ai_ui.layout.pid_layout import get_pid_component



# PID布局
def pid_layout():
    card = create_vertical_card("PID test")
    layout: QVBoxLayout = card._layout
    # layout.addWidget(QLabel("组件"))
    # layout.addWidget(QLabel("PID"))
    layout.addWidget(get_pid_component())
    return card


# 卡尔曼滤波布局
def kalman_filter_layout():
    layout = get_vertical_layout()
    layout.addWidget(QLabel("卡尔曼滤波"))
    return layout


# 主布局
def get_main_layout():
    layout = get_vertical_layout()
    layout.addWidget(pid_layout())
    layout.addLayout(kalman_filter_layout())
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