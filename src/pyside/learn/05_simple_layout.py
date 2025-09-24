"""
05. 简单布局 - QVBoxLayout 垂直布局示例
QVBoxLayout: 组件从上到下自动排列，全自动布局
"""
import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout

# 1. 创建应用程序实例
app = QApplication(sys.argv)

# 2. 创建主窗口
window = QWidget()
window.setWindowTitle("简单布局")  # 设置窗口标题
window.resize(400, 300)  # 设置窗口大小：宽400，高300

# 3. 创建垂直布局管理器
# QVBoxLayout: 垂直布局，组件从上到下自动排列
layout = QVBoxLayout()

# 4. 创建UI组件
label = QLabel("Hello World!")  # 创建文本标签
button = QPushButton("点击我")   # 创建第一个按钮

# 5. 将组件添加到布局中（按顺序从上到下）
layout.addWidget(label)   # 第1个：标签在最上面
layout.addWidget(button)  # 第2个：按钮在中间

# 6. 继续添加更多组件
button2 = QPushButton("点击我2")  # 创建第二个按钮
layout.addWidget(button2)  # 第3个：按钮在最下面，自动排列

# 7. 将布局应用到窗口
# 这一步很重要：告诉窗口使用这个布局来排列组件
window.setLayout(layout)

# 8. 显示窗口并运行程序
window.show()  # 显示窗口
sys.exit(app.exec())  # 进入事件循环，程序开始运行
