

import sys
from PySide6.QtWidgets import QApplication, QWidget
from pyside.basic.basic_layout import get_vertical_layout
from pyside.basic.basic_window import create_basic_window

from PySide6.QtWidgets import QLabel, QWidget
from pyside.basic.basic_layout import get_vertical_layout



# PID布局
def pid_layout():
    layout = get_vertical_layout()
    layout.addWidget(QLabel("PID"))
    return layout


# 卡尔曼滤波布局
def kalman_filter_layout():
    layout = get_vertical_layout()
    layout.addWidget(QLabel("卡尔曼滤波"))
    return layout


# 主布局
def get_main_layout():
    layout = get_vertical_layout()
    layout.addLayout(pid_layout())
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