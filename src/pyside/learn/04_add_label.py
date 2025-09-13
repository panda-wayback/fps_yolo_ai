"""
04. 添加标签
"""
import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("带标签的窗口")
window.resize(400, 300)

# 创建标签
label = QLabel("Hello World!", window)
label.move(150, 50)

# 创建按钮
button = QPushButton("点击我", window,
    # print 按钮被点击
    clicked = lambda: print("按钮被点击了")
    )
button.move(150, 100)

window.show()
sys.exit(app.exec())
