

import sys
from PySide6.QtWidgets import QApplication, QGroupBox, QWidget, QHBoxLayout
from data_center.models.input_monitor.subject import InputMonitorSubject
from pyside.UI.basic.basic_layout import get_vertical_layout
from pyside.UI.basic.basic_window import create_basic_window, create_scrollable_window
from pyside.UI.basic.multi_widget import add_widgets_to_vertical, add_layouts
from pyside.fps_ai_ui.component.mouse_driver.index import get_mouse_driver_component
from pyside.fps_ai_ui.component.pid_controller.index import get_pid_controller_component
from pyside.fps_ai_ui.component.screenshot.index import get_screenshot_component
from pyside.fps_ai_ui.component.target_selector.index import get_target_selector_component
from pyside.fps_ai_ui.component.yolo_model.index import get_yolo_model_component



# YOLO模型选择组件
def yolo_model_component() -> QGroupBox:
    return get_yolo_model_component()

# PID控制器组件
def pid_controller_component() -> QGroupBox:
    return get_pid_controller_component()

# 截图组件
def screenshot_component() -> QGroupBox:
    return get_screenshot_component()

# 目标选择器组件
def target_selector_component() -> QGroupBox:
    return get_target_selector_component()

# 鼠标驱动组件
def mouse_driver_component() -> QGroupBox:
    return get_mouse_driver_component()
# 主布局
def get_main_layout():
    # 设置主垂直布局
    main_layout = get_vertical_layout()
    
    # 创建两列布局
    columns_layout = QHBoxLayout()

    # 创建三列布局
    first_columns_layout = add_widgets_to_vertical(
        yolo_model_component(),                  # YOLO模型选择组件
       
        
    ) # 目标跟踪器组件

    
    # 左列布局
    second_columns_layout = add_widgets_to_vertical(
         screenshot_component(),                  # 截图组件
         mouse_driver_component(),                  # 鼠标驱动组件
    )
    
    # 右列布局  
    third_columns_layout = add_widgets_to_vertical(
        pid_controller_component(),                  # PID控制器组件
        target_selector_component(),                  # 目标选择器组件
       
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
    InputMonitorSubject.monitor_keyboard_press("p")
    app = QApplication(sys.argv)
    window = create_basic_window("FPS AI 控制台", 1200, 800)

    # 将布局直接设置到窗口中
    content_layout = get_main_layout()
    window.setLayout(content_layout)

    prompt_window(window)
    sys.exit(app.exec())


if __name__ == "__main__":
    main_window()