

import sys
from PySide6.QtWidgets import QApplication, QGroupBox, QWidget, QHBoxLayout
from pyside.UI.basic.basic_layout import get_vertical_layout
from pyside.UI.basic.basic_window import create_basic_window
from pyside.UI.basic.multi_widget import add_widgets_to_vertical, add_layouts
from pyside.fps_ai_ui.component.mouse_driver.index import get_mouse_driver_component
from pyside.fps_ai_ui.component.pid_controller.index import get_pid_controller_component
from pyside.fps_ai_ui.component.screenshot.index import get_screenshot_component
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

    )
    
    # 将列添加到水平布局
    add_layouts(columns_layout, first_columns_layout, second_columns_layout, third_columns_layout)
    
    # 将列布局添加到主布局
    main_layout.addLayout(columns_layout)
    
    return main_layout


def prompt_window(window: QWidget):
    try:
        """将窗口移动到指定屏幕"""
        app = QApplication.instance()  # 获取现有的 QApplication 实例
        screens = app.screens()
        if len(screens) > 1:
            screen = screens[1]  # 使用第二个屏幕
            window.move(screen.geometry().x(), screen.geometry().y())
        window.show()
       
    except Exception as e:
        print(f"❌ 将窗口移动到指定屏幕失败: {e}")

def init_state():
    from data_center.init_state import init_state
    init_state()
    pass


def main_window():
    print("🔧 步骤1: 创建 Qt 应用...")
    app = QApplication(sys.argv)
    print("✅ Qt 应用创建成功")
    
    print("🔧 步骤2: 创建窗口...")
    window = create_basic_window("FPS AI 控制台", 600, 400)
    print("✅ 窗口创建成功")

    print("🔧 步骤3: 创建布局...")
    content_layout = get_main_layout()
    window.setLayout(content_layout)
    print("✅ 布局设置成功")

    print("🔧 步骤4: 初始化状态...")
    init_state()
    print("✅ 初始化状态成功")

    print("🔧 步骤5: 显示窗口...")
    prompt_window(window)
    print("✅ 窗口显示成功，进入事件循环")
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main_window()