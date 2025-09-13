"""
22. 嵌套布局示例
展示复杂的嵌套布局结构
"""
import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                               QGridLayout, QPushButton, QLabel, QGroupBox, QTextEdit)

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("嵌套布局示例")
window.resize(700, 600)

# 主布局（垂直）
main_layout = QVBoxLayout()

# 1. 标题区域（水平布局）
header_layout = QHBoxLayout()
header_layout.addWidget(QLabel("标题区域"))
header_layout.addStretch()  # 添加弹性空间
header_layout.addWidget(QPushButton("设置"))

# 2. 内容区域（水平布局）
content_layout = QHBoxLayout()

# 2.1 左侧面板（垂直布局）
left_panel_layout = QVBoxLayout()
left_panel_layout.addWidget(QLabel("左侧面板"))
left_panel_layout.addWidget(QPushButton("按钮1"))
left_panel_layout.addWidget(QPushButton("按钮2"))
left_panel_layout.addWidget(QPushButton("按钮3"))

# 2.2 中间面板（网格布局）
middle_panel_layout = QGridLayout()
middle_panel_layout.addWidget(QLabel("中间面板"), 0, 0, 1, 2)
middle_panel_layout.addWidget(QPushButton("按钮A"), 1, 0)
middle_panel_layout.addWidget(QPushButton("按钮B"), 1, 1)
middle_panel_layout.addWidget(QPushButton("按钮C"), 2, 0)
middle_panel_layout.addWidget(QPushButton("按钮D"), 2, 1)

# 2.3 右侧面板（垂直布局）
right_panel_layout = QVBoxLayout()
right_panel_layout.addWidget(QLabel("右侧面板"))
right_panel_layout.addWidget(QTextEdit("文本区域"))
right_panel_layout.addWidget(QPushButton("保存"))

# 将子面板添加到内容布局
content_layout.addLayout(left_panel_layout)
content_layout.addLayout(middle_panel_layout)
content_layout.addLayout(right_panel_layout)

# 3. 底部区域（水平布局）
footer_layout = QHBoxLayout()
footer_layout.addWidget(QPushButton("取消"))
footer_layout.addStretch()
footer_layout.addWidget(QPushButton("确定"))

# 将所有布局添加到主布局
main_layout.addLayout(header_layout)
main_layout.addLayout(content_layout)
main_layout.addLayout(footer_layout)

# 设置主布局
window.setLayout(main_layout)

window.show()
sys.exit(app.exec())
