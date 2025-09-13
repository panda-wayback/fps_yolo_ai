"""
24. QGroupBox 样式示例
展示不同的 QGroupBox 标题样式
"""
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGroupBox, QLabel, QPushButton
from PySide6.QtCore import Qt

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("QGroupBox 样式示例")
window.resize(600, 500)

# 主布局
main_layout = QVBoxLayout()

# 1. 默认样式
default_group = QGroupBox("默认样式")
default_layout = QVBoxLayout()
default_layout.addWidget(QLabel("这是默认的 QGroupBox 样式"))
default_group.setLayout(default_layout)
main_layout.addWidget(default_group)

# 2. 自定义标题样式
styled_group = QGroupBox("自定义样式")
styled_group.setStyleSheet("""
    QGroupBox {
        font-size: 16px;
        font-weight: bold;
        color: #2c3e50;
        border: 2px solid #3498db;
        border-radius: 8px;
        margin: 10px;
        padding-top: 15px;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 8px 0 8px;
        background-color: white;
    }
""")
styled_layout = QVBoxLayout()
styled_layout.addWidget(QLabel("这是自定义样式的 QGroupBox"))
styled_group.setLayout(styled_layout)
main_layout.addWidget(styled_group)

# 3. 扁平化样式
flat_group = QGroupBox("扁平化样式")
flat_group.setStyleSheet("""
    QGroupBox {
        font-size: 14px;
        font-weight: bold;
        color: #34495e;
        border: 1px solid #bdc3c7;
        border-radius: 5px;
        margin: 8px;
        padding-top: 12px;
        background-color: #ecf0f1;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 15px;
        padding: 0 6px 0 6px;
        background-color: #ecf0f1;
    }
""")
flat_layout = QVBoxLayout()
flat_layout.addWidget(QLabel("这是扁平化样式的 QGroupBox"))
flat_group.setLayout(flat_layout)
main_layout.addWidget(flat_group)

# 4. 现代卡片样式
modern_group = QGroupBox("现代卡片样式")
modern_group.setStyleSheet("""
    QGroupBox {
        font-size: 18px;
        font-weight: bold;
        color: #2c3e50;
        border: none;
        border-radius: 12px;
        margin: 15px;
        padding-top: 20px;
        background-color: #ffffff;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 20px;
        padding: 0 10px 0 10px;
        background-color: #ffffff;
        color: #e74c3c;
    }
""")
modern_layout = QVBoxLayout()
modern_layout.addWidget(QLabel("这是现代卡片样式的 QGroupBox"))
modern_layout.addWidget(QPushButton("按钮"))
modern_group.setLayout(modern_layout)
main_layout.addWidget(modern_group)

# 5. 深色主题样式
dark_group = QGroupBox("深色主题样式")
dark_group.setStyleSheet("""
    QGroupBox {
        font-size: 16px;
        font-weight: bold;
        color: #ecf0f1;
        border: 2px solid #34495e;
        border-radius: 8px;
        margin: 10px;
        padding-top: 15px;
        background-color: #2c3e50;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 8px 0 8px;
        background-color: #2c3e50;
        color: #3498db;
    }
""")
dark_layout = QVBoxLayout()
dark_layout.addWidget(QLabel("这是深色主题样式的 QGroupBox"))
dark_group.setLayout(dark_layout)
main_layout.addWidget(dark_group)

# 6. 渐变样式
gradient_group = QGroupBox("渐变样式")
gradient_group.setStyleSheet("""
    QGroupBox {
        font-size: 16px;
        font-weight: bold;
        color: white;
        border: 2px solid #9b59b6;
        border-radius: 10px;
        margin: 12px;
        padding-top: 18px;
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                                   stop:0 #9b59b6, stop:1 #8e44ad);
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 15px;
        padding: 0 10px 0 10px;
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                                   stop:0 #9b59b6, stop:1 #8e44ad);
    }
""")
gradient_layout = QVBoxLayout()
gradient_layout.addWidget(QLabel("这是渐变样式的 QGroupBox"))
gradient_group.setLayout(gradient_layout)
main_layout.addWidget(gradient_group)

window.setLayout(main_layout)
window.show()
sys.exit(app.exec())
