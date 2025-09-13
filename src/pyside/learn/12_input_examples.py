"""
12. 输入组件示例
展示各种输入控件：文本框、密码框、多行文本、数字输入等

关键概念：
- QGroupBox 创建卡片效果，将相关组件分组
- 每个卡片有标题和边框，形成独立的视觉区域
- 卡片内部使用独立的布局管理组件
"""
import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                               QLabel, QPushButton, QLineEdit, QTextEdit, 
                               QSpinBox, QDoubleSpinBox, QComboBox, QCheckBox, 
                               QRadioButton, QGroupBox)

# 1. 创建应用程序实例
app = QApplication(sys.argv)

# 2. 创建主窗口
window = QWidget()
window.setWindowTitle("输入组件示例")
window.resize(500, 600)

# 3. 创建主布局（垂直布局）
main_layout = QVBoxLayout()

# 4. 创建第一个卡片：文本输入组
# QGroupBox 创建卡片效果，有标题和边框
text_group = QGroupBox("文本输入")  # 卡片标题
text_layout = QVBoxLayout()  # 卡片内部布局

# 4.1 单行文本输入
text_layout.addWidget(QLabel("单行文本:"))
single_line = QLineEdit()
single_line.setPlaceholderText("请输入单行文本...")
text_layout.addWidget(single_line)

# 4.2 密码输入
text_layout.addWidget(QLabel("密码输入:"))
password = QLineEdit()
password.setEchoMode(QLineEdit.Password)  # 密码模式，输入内容显示为星号
password.setPlaceholderText("请输入密码...")
text_layout.addWidget(password)

# 4.3 多行文本输入
text_layout.addWidget(QLabel("多行文本:"))
multi_line = QTextEdit()
multi_line.setPlaceholderText("请输入多行文本...")
multi_line.setMaximumHeight(100)  # 限制高度
text_layout.addWidget(multi_line)

# 4.4 将布局应用到卡片，然后将卡片添加到主布局
text_group.setLayout(text_layout)  # 卡片内部布局
main_layout.addWidget(text_group)  # 卡片添加到主布局

# 5. 创建第二个卡片：数字输入组
# 另一个独立的卡片区域
number_group = QGroupBox("数字输入")  # 卡片标题
number_layout = QVBoxLayout()  # 卡片内部布局

# 5.1 整数输入
number_layout.addWidget(QLabel("整数输入:"))
int_spin = QSpinBox()
int_spin.setRange(0, 100)  # 设置范围 0-100
int_spin.setValue(50)      # 设置默认值
number_layout.addWidget(int_spin)

# 5.2 小数输入
number_layout.addWidget(QLabel("小数输入:"))
double_spin = QDoubleSpinBox()
double_spin.setRange(0.0, 100.0)  # 设置范围 0.0-100.0
double_spin.setValue(25.5)        # 设置默认值
double_spin.setDecimals(2)        # 设置小数位数
number_layout.addWidget(double_spin)

# 5.3 将布局应用到卡片，然后将卡片添加到主布局
number_group.setLayout(number_layout)  # 卡片内部布局
main_layout.addWidget(number_group)    # 卡片添加到主布局

# 6. 创建第三个卡片：选择输入组
# 第三个独立的卡片区域
choice_group = QGroupBox("选择输入")  # 卡片标题
choice_layout = QVBoxLayout()  # 卡片内部布局

# 6.1 下拉选择
choice_layout.addWidget(QLabel("下拉选择:"))
combo = QComboBox()
combo.addItems(["选项1", "选项2", "选项3", "选项4"])
combo.setCurrentText("选项2")  # 设置默认选项
choice_layout.addWidget(combo)

# 6.2 复选框（可以多选）
choice_layout.addWidget(QLabel("复选框:"))
checkbox1 = QCheckBox("选项A")
checkbox2 = QCheckBox("选项B")
checkbox3 = QCheckBox("选项C")
checkbox1.setChecked(True)  # 默认选中
choice_layout.addWidget(checkbox1)
choice_layout.addWidget(checkbox2)
choice_layout.addWidget(checkbox3)

# 6.3 单选按钮（只能选一个）
choice_layout.addWidget(QLabel("单选按钮:"))
radio1 = QRadioButton("选项1")
radio2 = QRadioButton("选项2")
radio3 = QRadioButton("选项3")
radio2.setChecked(True)  # 默认选中
choice_layout.addWidget(radio1)
choice_layout.addWidget(radio2)
choice_layout.addWidget(radio3)

# 6.4 将布局应用到卡片，然后将卡片添加到主布局
choice_group.setLayout(choice_layout)  # 卡片内部布局
main_layout.addWidget(choice_group)    # 卡片添加到主布局

# 7. 创建按钮组（不是卡片，直接添加到主布局）
button_layout = QHBoxLayout()
get_values_btn = QPushButton("获取所有值")
clear_btn = QPushButton("清空所有")
button_layout.addWidget(get_values_btn)
button_layout.addWidget(clear_btn)
main_layout.addLayout(button_layout)

# 8. 按钮事件处理函数
def get_all_values():
    """获取所有输入值"""
    print("=== 所有输入值 ===")
    print(f"单行文本: {single_line.text()}")
    print(f"密码: {password.text()}")
    print(f"多行文本: {multi_line.toPlainText()}")
    print(f"整数: {int_spin.value()}")
    print(f"小数: {double_spin.value()}")
    print(f"下拉选择: {combo.currentText()}")
    print(f"复选框A: {checkbox1.isChecked()}")
    print(f"复选框B: {checkbox2.isChecked()}")
    print(f"复选框C: {checkbox3.isChecked()}")
    print(f"单选按钮: {radio1.isChecked()}, {radio2.isChecked()}, {radio3.isChecked()}")

def clear_all():
    """清空所有输入"""
    single_line.clear()
    password.clear()
    multi_line.clear()
    int_spin.setValue(0)
    double_spin.setValue(0.0)
    combo.setCurrentIndex(0)
    checkbox1.setChecked(False)
    checkbox2.setChecked(False)
    checkbox3.setChecked(False)
    radio1.setChecked(False)
    radio2.setChecked(False)
    radio3.setChecked(False)

# 9. 连接按钮事件
get_values_btn.clicked.connect(get_all_values)
clear_btn.clicked.connect(clear_all)

# 10. 设置主布局并显示窗口
window.setLayout(main_layout)
window.show()
sys.exit(app.exec())
