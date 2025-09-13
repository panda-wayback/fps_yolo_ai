"""
16. 网格布局 - 按钮示例
展示网格布局中按钮的使用
"""
import sys
from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("网格布局 - 按钮示例")
window.resize(400, 300)

# 创建网格布局
layout = QGridLayout()

# 创建按钮并添加到网格
buttons = []
for row in range(3):
    for col in range(3):
        btn = QPushButton(f"({row},{col})")
        btn.clicked.connect(lambda checked, r=row, c=col: print(f"按钮 ({r},{c}) 被点击"))
        layout.addWidget(btn, row, col)
        buttons.append(btn)

# 设置布局
window.setLayout(layout)

window.show()
sys.exit(app.exec())
