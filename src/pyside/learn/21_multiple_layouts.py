"""
21. 多个布局示例
展示一个窗口中使用多个布局的方法

关键概念：
- 一个窗口只能有一个主布局
- 但可以通过嵌套的方式使用多个子布局
- 使用 addLayout() 将子布局添加到主布局中
"""
import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                               QGridLayout, QPushButton, QLabel, QGroupBox)

# 1. 创建应用程序实例
app = QApplication(sys.argv)

# 2. 创建主窗口
window = QWidget()
window.setWindowTitle("多个布局示例")
window.resize(600, 500)

# 3. 创建主布局（垂直布局）
# 主布局负责管理整个窗口的布局结构
main_layout = QVBoxLayout()

# 4. 创建第一个子布局：顶部布局（水平布局）
# 用于在窗口顶部水平排列组件
top_layout = QHBoxLayout()
top_layout.addWidget(QLabel("顶部左侧"))
top_layout.addWidget(QLabel("顶部中间"))
top_layout.addWidget(QLabel("顶部右侧"))

# 5. 创建第二个子布局：中间布局（网格布局）
# 用于在窗口中间以网格形式排列组件
middle_layout = QGridLayout()
# 网格布局语法：addWidget(组件, 行, 列)
middle_layout.addWidget(QLabel("(0,0)"), 0, 0)  # 第0行第0列
middle_layout.addWidget(QLabel("(0,1)"), 0, 1)  # 第0行第1列
middle_layout.addWidget(QLabel("(1,0)"), 1, 0)  # 第1行第0列
middle_layout.addWidget(QLabel("(1,1)"), 1, 1)  # 第1行第1列

# 6. 创建第三个子布局：底部布局（水平布局）
# 用于在窗口底部水平排列按钮
bottom_layout = QHBoxLayout()
bottom_layout.addWidget(QPushButton("底部按钮1"))
bottom_layout.addWidget(QPushButton("底部按钮2"))
bottom_layout.addWidget(QPushButton("底部按钮3"))

# 7. 将子布局添加到主布局中
# 这是关键步骤：使用 addLayout() 将子布局添加到主布局
main_layout.addLayout(top_layout)      # 顶部布局添加到主布局
main_layout.addLayout(middle_layout)   # 中间布局添加到主布局
main_layout.addLayout(bottom_layout)   # 底部布局添加到主布局

# 8. 将主布局应用到窗口
# 这一步告诉窗口使用这个布局来管理所有组件
window.setLayout(main_layout)

# 9. 显示窗口并运行程序
window.show()
sys.exit(app.exec())
