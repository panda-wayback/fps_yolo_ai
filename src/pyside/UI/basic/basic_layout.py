import sys
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox

from pyside.UI.basic.basic_window import create_basic_window


# 获取垂直布局
def get_vertical_layout():
    return QVBoxLayout()

# 获取水平布局
def get_horizontal_layout():
    return QHBoxLayout()

# 获取网格布局
def get_grid_layout():
    return QGridLayout()

# 创建卡片组件（直接返回组件，更合理）
def create_card(title="卡片标题"):
    """创建卡片组件 - 直接返回组件，使用更简单"""
    group = QGroupBox(title)  # 创建卡片容器
    layout = get_horizontal_layout()    # 卡片内部布局
    group.setLayout(layout)   # 将布局应用到卡片
    group._layout = layout    # 将布局存储到组件中
    return group  # 直接返回组件

# 创建带卡片的垂直布局
def create_vertical_card(title="垂直卡片"):
    """创建垂直卡片组件 - 直接返回组件"""
    group = QGroupBox(title)
    layout = get_vertical_layout()
    group.setLayout(layout)
    group._layout = layout
    return group

# 创建带卡片的水平布局
def create_horizontal_card(title="水平卡片") -> QGroupBox:
    """创建水平卡片组件 - 直接返回组件"""
    group = QGroupBox(title)
    layout = QHBoxLayout()
    group.setLayout(layout)
    group._layout = layout
    return group

# 创建带卡片的网格布局
def create_grid_card(title="网格卡片"):
    """创建网格卡片组件 - 直接返回组件"""
    group = QGroupBox(title)
    layout = QGridLayout()
    group.setLayout(layout)
    group._layout = layout
    return group


def main():
    """主函数 - 展示卡片布局效果"""
    app = QApplication(sys.argv)
    window = create_basic_window()
    
    # 创建主布局
    main_layout = get_vertical_layout()
    
    # 创建第一个卡片：垂直卡片
    card1 = create_vertical_card("垂直卡片")
    card1._layout.addWidget(QLabel("这是垂直卡片的内容"))
    card1._layout.addWidget(QLabel("可以添加多个组件"))
    main_layout.addWidget(card1)  # 直接添加组件
    
    # 创建第二个卡片：水平卡片
    card2 = create_horizontal_card("水平卡片")
    card2._layout.addWidget(QLabel("左"))
    card2._layout.addWidget(QLabel("中"))
    card2._layout.addWidget(QLabel("右"))
    main_layout.addWidget(card2)  # 直接添加组件
    
    # 创建第三个卡片：网格卡片
    card3 = create_grid_card("网格卡片")
    card3._layout.addWidget(QLabel("(0,0)"), 0, 0)
    card3._layout.addWidget(QLabel("(0,1)"), 0, 1)
    card3._layout.addWidget(QLabel("(1,0)"), 1, 0)
    card3._layout.addWidget(QLabel("(1,1)"), 1, 1)
    main_layout.addWidget(card3)  # 直接添加组件
    
    # 设置布局
    window.setLayout(main_layout)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()