"""
23. 动态布局示例
展示如何动态添加和移除布局
"""
import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                               QPushButton, QLabel, QGroupBox)

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("动态布局示例")
window.resize(500, 400)

# 主布局
main_layout = QVBoxLayout()

# 控制按钮
control_layout = QHBoxLayout()
add_btn = QPushButton("添加布局")
remove_btn = QPushButton("移除布局")
clear_btn = QPushButton("清空所有")

control_layout.addWidget(add_btn)
control_layout.addWidget(remove_btn)
control_layout.addWidget(clear_btn)

# 动态布局容器
dynamic_layout = QVBoxLayout()

# 布局计数器
layout_count = 0

def add_layout():
    """添加新布局"""
    global layout_count
    layout_count += 1
    
    # 创建新的水平布局
    new_layout = QHBoxLayout()
    new_layout.addWidget(QLabel(f"布局 {layout_count}"))
    new_layout.addWidget(QPushButton(f"按钮 {layout_count}"))
    
    # 添加到动态布局容器
    dynamic_layout.addLayout(new_layout)
    
    print(f"添加了布局 {layout_count}")

def remove_layout():
    """移除最后一个布局"""
    global layout_count
    if layout_count > 0:
        # 获取最后一个布局
        last_layout = dynamic_layout.takeAt(dynamic_layout.count() - 1)
        if last_layout:
            # 清理布局中的组件
            while last_layout.count():
                child = last_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
            last_layout.deleteLater()
        
        layout_count -= 1
        print(f"移除了布局，剩余 {layout_count} 个")

def clear_all():
    """清空所有动态布局"""
    global layout_count
    while dynamic_layout.count():
        item = dynamic_layout.takeAt(0)
        if item.layout():
            # 清理布局
            while item.layout().count():
                child = item.layout().takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
            item.layout().deleteLater()
        elif item.widget():
            item.widget().deleteLater()
    
    layout_count = 0
    print("清空了所有布局")

# 连接按钮事件
add_btn.clicked.connect(add_layout)
remove_btn.clicked.connect(remove_layout)
clear_btn.clicked.connect(clear_all)

# 添加到主布局
main_layout.addLayout(control_layout)
main_layout.addLayout(dynamic_layout)

# 设置主布局
window.setLayout(main_layout)

window.show()
sys.exit(app.exec())
