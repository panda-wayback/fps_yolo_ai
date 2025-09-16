#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的YOLO模型选择组件
只提供文件选择功能，获取模型路径
"""

from PySide6.QtWidgets import (QHBoxLayout, QPushButton, QLabel, 
                               QFileDialog, QLineEdit)
from PySide6.QtCore import Qt
from pyside.UI.basic.basic_layout import create_vertical_card
import os

from singleton_classes.yolo_recog.yolo_recog import YoloRecog


def create_yolo_model_selector():
    """
    创建YOLO模型选择组件
    
    Returns:
        QGroupBox: YOLO模型选择组件
    """
    # 创建主容器
    group = create_vertical_card("YOLO模型选择")
    layout = group._layout
    
    # 模型路径输入框
    path_label = QLabel("模型路径:")
    path_input = QLineEdit()
    path_input.setPlaceholderText("请选择YOLO模型文件...")
    path_input.setReadOnly(True)
    
    # 选择按钮
    select_btn = QPushButton("选择模型")
    
    # 清除按钮
    clear_btn = QPushButton("清除")

    # 加载按钮
    load_btn = QPushButton("加载模型")
    
    # 布局
    path_layout = QHBoxLayout()
    path_layout.addWidget(path_label)
    path_layout.addWidget(path_input)
    
    button_layout = QHBoxLayout()
    button_layout.addWidget(load_btn)
    button_layout.addWidget(select_btn)
    button_layout.addWidget(clear_btn)
    

    layout.addLayout(path_layout)
    layout.addLayout(button_layout)
    
    # 选择文件功能
    def select_model():
        """选择模型文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            None,
            "选择YOLO模型文件",
            "",
            "模型文件 (*.pt *.onnx *.engine);;所有文件 (*.*)"
        )
        
        if file_path:
            path_input.setText(file_path)
            print(f"✅ 选择模型: {os.path.basename(file_path)}")
    
    # 清除路径功能
    def clear_path():
        """清除选择的路径"""
        path_input.clear()
        print("🔄 清除模型路径")
    
    # 加载模型功能
    def load_model():
        """加载模型"""
        model_path = path_input.text()
        if model_path:
            print(f"✅ 加载模型: {os.path.basename(model_path)}")
        if  YoloRecog().load_model(model_path):
            YoloRecog().start(model_path)
            print("✅ 模型加载成功")
            print(f"模型信息: {YoloRecog().get_model_info()}")
        else:
            print("❌ 模型加载失败")
    
    
    # 连接按钮事件
    load_btn.clicked.connect(load_model)
    select_btn.clicked.connect(select_model)
    clear_btn.clicked.connect(clear_path)
    
    
    # 存储引用到组件
    group.path_input = path_input
    group.select_model = select_model
    group.clear_path = clear_path
    
    return group


def get_yolo_model_selector():
    """
    获取YOLO模型选择组件
    
    Returns:
        QGroupBox: YOLO模型选择组件
    """
    return create_yolo_model_selector()
