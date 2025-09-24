#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的YOLO模型选择组件
只提供文件选择功能，获取模型路径
"""

from PySide6.QtWidgets import QPushButton, QFileDialog
from pyside.UI.basic.basic_layout import create_vertical_card
import os

from data_center.models.yolo_model.subject import YoloSubject


def create_yolo_model_selector():
    """
    创建YOLO模型选择组件
    
    Returns:
        QGroupBox: YOLO模型选择组件
    """
    # 创建主容器
    group = create_vertical_card("YOLO模型选择")
    layout = group._layout
    
    # 选择并加载模型按钮
    load_btn = QPushButton("选择并加载模型")
    
    layout.addWidget(load_btn)
    
    # 选择并加载模型功能
    def select_and_load_model():
        """选择并加载模型文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            None,
            "选择YOLO模型文件",
            "",
            "模型文件 (*.pt *.onnx *.engine);;所有文件 (*.*)"
        )
        
        if not file_path:
            return
            
        if not os.path.exists(file_path):
            print(f"❌ 模型文件不存在: {file_path}")
            return
            
        print(f"🔄 正在加载模型: {os.path.basename(file_path)}")
        try:
            # 通过话题发送模型路径
            YoloSubject.send_model_path(file_path)
            print("✅ 模型加载请求已发送")
        except Exception as e:
            print(f"❌ 模型加载失败: {str(e)}")
    
    # 连接按钮事件
    load_btn.clicked.connect(select_and_load_model)
    
    return group

def get_yolo_model_selector():
    """
    获取YOLO模型选择组件
    
    Returns:
        QGroupBox: YOLO模型选择组件
    """
    return create_yolo_model_selector()
