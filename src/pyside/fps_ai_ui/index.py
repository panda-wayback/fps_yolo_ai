

import sys
from PySide6.QtWidgets import QApplication, QGroupBox, QWidget, QHBoxLayout
from pyside.UI.basic.basic_layout import get_vertical_layout
from pyside.UI.basic.basic_window import create_scrollable_window
from pyside.UI.basic.multi_widget import add_widgets_to_vertical, add_layouts
from pyside.fps_ai_ui.component.img_show.index import get_img_show_component
from pyside.fps_ai_ui.component.move_mouse.index import get_move_mouse_component
from pyside.fps_ai_ui.component.pid_component.index import get_pid_component
from pyside.fps_ai_ui.component.yolo_model.index import get_yolo_model_component
from pyside.fps_ai_ui.component.target_tracker.index import get_target_tracker_component
from pyside.fps_ai_ui.component.model_class_select.index import get_model_class_selector



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

# 目标跟踪器组件
def target_tracker_component() -> QGroupBox:
    return get_target_tracker_component()

# 模型类别选择组件
def model_class_selector_component() -> QGroupBox:
    return get_model_class_selector()


# 主布局
def get_main_layout():
    # 设置主垂直布局
    main_layout = get_vertical_layout()
    
    # 创建两列布局
    columns_layout = QHBoxLayout()

    # 创建三列布局
    first_columns_layout = add_widgets_to_vertical(
        img_show_component(),                    # 图片展示组件
        yolo_model_component(),                  # YOLO模型选择组件
        model_class_selector_component(),        # 模型类别选择组件
        pid_component()                          # PID参数控制组件

    ) # 目标跟踪器组件

    
    # 左列布局
    second_columns_layout = add_widgets_to_vertical(
        target_tracker_component(),
    )
    
    # 右列布局  
    third_columns_layout = add_widgets_to_vertical(
        
        move_mouse_component()   # 鼠标控制组件
    )
    
    # 将列添加到水平布局
    add_layouts(columns_layout, first_columns_layout, second_columns_layout, third_columns_layout)
    
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
    window = create_scrollable_window()

    # 将布局设置到内容容器中
    content_layout = get_main_layout()
    window.content_widget.setLayout(content_layout)

    prompt_window(window)
    sys.exit(app.exec())


if __name__ == "__main__":
    main_window()