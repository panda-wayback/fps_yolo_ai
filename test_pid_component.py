#!/usr/bin/env python3
"""
PID控制器组件测试脚本
"""

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget
from pyside.fps_ai_ui.component.pid_controller.index import get_pid_controller_component


def main():
    """主函数"""
    print("=== PID控制器组件测试 ===")
    
    # 创建应用程序
    app = QApplication(sys.argv)
    
    # 创建主窗口
    window = QWidget()
    window.setWindowTitle("PID控制器组件测试")
    window.setGeometry(100, 100, 800, 600)
    
    # 创建布局
    layout = QVBoxLayout(window)
    
    # 创建PID控制器组件
    print("创建PID控制器组件...")
    pid_component = get_pid_controller_component()
    
    # 添加到布局
    layout.addWidget(pid_component)
    
    # 显示窗口
    window.show()
    print("PID控制器组件已启动")
    print("请测试以下功能：")
    print("1. 调节Kp、Ki、Kd参数")
    print("2. 修改采样时间")
    print("3. 点击应用按钮")
    print("4. 观察状态显示")
    print("5. 查看控制日志")
    
    # 运行应用程序
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
