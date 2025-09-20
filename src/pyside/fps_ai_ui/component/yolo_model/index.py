import sys
from PySide6.QtWidgets import QApplication, QHBoxLayout
from pyside.UI.basic.basic_layout import create_vertical_card
from pyside.UI.basic.basic_window import create_scrollable_window
from pyside.fps_ai_ui.component.yolo_model.component.yolo_model_selector import get_yolo_model_selector
from pyside.fps_ai_ui.component.yolo_model.component.yolo_model_state import get_yolo_model_state
from pyside.fps_ai_ui.component.yolo_model.component.yolo_classes_selector import get_yolo_classes_selector
from pyside.fps_ai_ui.component.yolo_model.component.yolo_marked_image import get_yolo_marked_image


def get_yolo_model_selector_component():
    """
    创建YOLO模型选择组件
    
    Returns:
        QGroupBox: YOLO模型选择组件
    """
    return get_yolo_model_selector()


def get_yolo_model_state_component():
    """
    创建YOLO模型状态组件
    
    Returns:
        QGroupBox: YOLO模型状态组件
    """
    return get_yolo_model_state()


def get_yolo_classes_selector_component():
    """
    创建YOLO类别选择组件
    
    Returns:
        QGroupBox: YOLO类别选择组件
    """
    return get_yolo_classes_selector()


def get_yolo_marked_image_component():
    """
    创建YOLO标记图片显示组件
    
    Returns:
        QGroupBox: YOLO标记图片显示组件
    """
    return get_yolo_marked_image()


def get_yolo_model_component():
    # 创建垂直布局 
    # create_vertical_card

    # 上半部分：状态和类别选择
    top_layout = QHBoxLayout()
    top_layout.addWidget(get_yolo_model_state_component(), 1)       # 拉伸因子为1
    top_layout.addWidget(get_yolo_classes_selector_component(), 1)  # 拉伸因子为1

    # 下半部分：标记图片显示
    bottom_layout = QHBoxLayout()
    bottom_layout.addWidget(get_yolo_marked_image_component(), 1)   # 拉伸因子为1
    
    group = create_vertical_card()
    group._layout.addWidget(get_yolo_model_selector_component())
    group._layout.addLayout(top_layout)
    group._layout.addLayout(bottom_layout)

    return group 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = create_scrollable_window()
    # 注意：setLayout 需要传入 QLayout，而不是 QGroupBox
    # get_yolo_model_component() 返回的是 QGroupBox，需要将其作为 widget 添加到 content_widget 的布局中
    # 假设 content_widget 已经有布局（如 QVBoxLayout），否则需要先设置布局
    yolo_model_group = get_yolo_model_component()
    # 检查 content_widget 是否已有布局
    if window.content_widget.layout() is None:
        from PySide6.QtWidgets import QVBoxLayout
        window.content_widget.setLayout(QVBoxLayout())
    window.content_widget.layout().addWidget(yolo_model_group)
    window.show()
    sys.exit(app.exec())