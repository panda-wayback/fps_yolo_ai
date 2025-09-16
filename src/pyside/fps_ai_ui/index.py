

import sys
from PySide6.QtWidgets import QApplication, QGroupBox, QWidget, QVBoxLayout, QHBoxLayout
from pyside.UI.basic.basic_layout import get_vertical_layout
from pyside.UI.basic.basic_window import create_basic_window
from pyside.fps_ai_ui.component.img_show.index import get_img_show_component
from pyside.fps_ai_ui.component.move_mouse.index import get_move_mouse_component
from pyside.fps_ai_ui.component.pid_component.index import get_pid_component
from pyside.fps_ai_ui.component.yolo_model.index import get_yolo_model_component



# PID参数控制组件
def pid_component() -> QGroupBox:
    return get_pid_component()

# YOLO模型选择组件
def yolo_model_component() -> QGroupBox:
    return get_yolo_model_component()

# 图片展示组件
def img_show_component() -> QGroupBox:
    return get_img_show_component()

# 鼠标控制组件
def move_mouse_component() -> QGroupBox:
    return get_move_mouse_component()


# 主布局
def get_main_layout():
    # 设置主垂直布局
    main_layout = get_vertical_layout()
    
    # 创建两列布局
    columns_layout = QHBoxLayout()
    
    # 左列布局
    left_column = QVBoxLayout()
    left_column.addWidget(move_mouse_component()) # 

    
    # 右列布局  
    right_column = QVBoxLayout()
    right_column.addWidget(img_show_component())   # 图片展示组件
    
    right_column.addWidget(yolo_model_component())  # YOLO模型选择组件
    right_column.addWidget(pid_component())         # PID参数控制组件
    
    # 将两列添加到水平布局
    columns_layout.addLayout(left_column)
    columns_layout.addLayout(right_column)
    
    # 将列布局添加到主布局
    main_layout.addLayout(columns_layout)
    
    return main_layout


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