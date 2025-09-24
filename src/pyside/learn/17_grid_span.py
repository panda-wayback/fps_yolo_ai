"""
17. 网格布局 - 跨行跨列示例
展示网格布局中跨行跨列的使用
"""
import sys
from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLabel, QTextEdit

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("网格布局 - 跨行跨列示例")
window.resize(500, 400)

# 创建网格布局
layout = QGridLayout()

# 添加组件到网格中
# 格式：layout.addWidget(组件, 行, 列, 跨行数, 跨列数)

# 第一行：标题跨3列
title = QLabel("网格布局跨行跨列示例")
title.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px;")
layout.addWidget(title, 0, 0, 1, 3)

# 第二行：按钮1，按钮2，按钮3
layout.addWidget(QPushButton("按钮1"), 1, 0)
layout.addWidget(QPushButton("按钮2"), 1, 1)
layout.addWidget(QPushButton("按钮3"), 1, 2)

# 第三行：文本区域跨2列
text_area = QTextEdit()
text_area.setPlaceholderText("这是一个跨2列的文本区域")
text_area.setMaximumHeight(100)
layout.addWidget(text_area, 2, 0, 1, 2)

# 第三行：按钮4（跨1列）
layout.addWidget(QPushButton("按钮4"), 2, 2)

# 第四行：按钮5跨3列
wide_btn = QPushButton("这个按钮跨3列")
wide_btn.setStyleSheet("background-color: #3498db; color: white; padding: 10px;")
layout.addWidget(wide_btn, 3, 0, 1, 3)

# 第五行：按钮6跨2行
tall_btn = QPushButton("跨2行\n按钮")
tall_btn.setStyleSheet("background-color: #e74c3c; color: white; padding: 10px;")
layout.addWidget(tall_btn, 4, 0, 2, 1)

# 第五行：按钮7和按钮8
layout.addWidget(QPushButton("按钮7"), 4, 1)
layout.addWidget(QPushButton("按钮8"), 4, 2)

# 第六行：按钮9和按钮10
layout.addWidget(QPushButton("按钮9"), 5, 1)
layout.addWidget(QPushButton("按钮10"), 5, 2)

# 设置布局
window.setLayout(layout)

window.show()
sys.exit(app.exec())
