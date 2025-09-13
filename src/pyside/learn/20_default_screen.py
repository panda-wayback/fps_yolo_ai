"""
20. 默认屏幕显示示例
展示如何设置窗口默认显示在指定屏幕
"""
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt

def create_window_on_screen(screen_index=1):
    """在指定屏幕创建窗口"""
    app = QApplication(sys.argv)
    
    # 获取屏幕信息
    screens = app.screens()
    print(f"检测到 {len(screens)} 个屏幕")
    
    # 选择屏幕
    if screen_index < len(screens):
        target_screen = screens[screen_index]
        print(f"选择屏幕 {screen_index}: {target_screen.name()}")
    else:
        target_screen = screens[0]  # 默认第一个屏幕
        print(f"屏幕索引超出范围，使用默认屏幕: {target_screen.name()}")
    
    # 创建窗口
    window = QWidget()
    window.setWindowTitle(f"显示在屏幕 {screen_index}")
    window.resize(400, 300)
    
    # 设置窗口在指定屏幕显示
    window.setScreen(target_screen)
    
    # 计算窗口在屏幕中的位置（居中）
    screen_geometry = target_screen.geometry()
    window_geometry = window.geometry()
    
    x = screen_geometry.x() + (screen_geometry.width() - window_geometry.width()) // 2
    y = screen_geometry.y() + (screen_geometry.height() - window_geometry.height()) // 2
    
    window.move(x, y)
    
    # 创建布局
    layout = QVBoxLayout()
    window.setLayout(layout)
    
    # 添加标签
    info_label = QLabel(f"当前屏幕: {target_screen.name()}\n分辨率: {screen_geometry.width()}x{screen_geometry.height()}")
    info_label.setAlignment(Qt.AlignCenter)
    layout.addWidget(info_label)
    
    # 添加按钮
    btn = QPushButton("关闭窗口")
    btn.clicked.connect(window.close)
    layout.addWidget(btn)
    
    return app, window

def main():
    """主函数"""
    # 在屏幕1显示窗口（索引从0开始，所以1是第二个屏幕）
    app, window = create_window_on_screen(1)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
