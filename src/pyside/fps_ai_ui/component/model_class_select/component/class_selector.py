#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模型类别选择组件
用于选择要识别的YOLO模型类别
"""

from PySide6.QtWidgets import (QHBoxLayout, QPushButton, QLabel, 
                               QListWidget, QListWidgetItem)
from PySide6.QtCore import Qt, QTimer
from pyside.UI.basic.basic_layout import create_vertical_card
from singleton_classes.data_center import DataCenter


def create_class_selector():
    """
    创建类别选择组件
    
    Returns:
        QGroupBox: 类别选择组件
    """
    # 创建主容器
    group = create_vertical_card("类别选择")
    layout = group._layout
    
    # 状态显示
    status_label = QLabel("等待模型加载...")
    status_label.setStyleSheet("""
        QLabel {
            color: #333333; 
            font-weight: bold; 
            font-size: 12px;
            padding: 5px;
            background-color: #f0f0f0;
            border-radius: 3px;
        }
    """)
    layout.addWidget(status_label)
    
    # 类别列表
    class_list = QListWidget()
    class_list.setMaximumHeight(150)
    class_list.setMinimumHeight(100)
    class_list.setStyleSheet("""
        QListWidget {
            border: 1px solid #cccccc;
            border-radius: 5px;
            background-color: white;
        }
        QListWidget::item {
            padding: 5px;
            border-bottom: 1px solid #eeeeee;
        }
        QListWidget::item:selected {
            background-color: #e3f2fd;
        }
    """)
    layout.addWidget(class_list)
    
    # 控制按钮
    select_all_btn = QPushButton("全选")
    clear_all_btn = QPushButton("清空")
    apply_btn = QPushButton("应用选择")
    
    # 按钮样式
    select_all_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; }")
    clear_all_btn.setStyleSheet("QPushButton { background-color: #f44336; color: white; }")
    apply_btn.setStyleSheet("QPushButton { background-color: #2196F3; color: white; }")
    
    # 按钮布局
    btn_layout = QHBoxLayout()
    btn_layout.addWidget(select_all_btn)
    btn_layout.addWidget(clear_all_btn)
    btn_layout.addWidget(apply_btn)
    layout.addLayout(btn_layout)
    
    # 选择信息显示
    info_label = QLabel("已选择: 0 个类别")
    info_label.setStyleSheet("""
        QLabel {
            color: #333333;
            font-size: 11px;
            padding: 3px;
        }
    """)
    layout.addWidget(info_label)
    
    # 定时器用于更新显示
    update_timer = QTimer()
    update_timer.timeout.connect(lambda: update_display())
    
    def update_display():
        """更新显示内容"""
        state = DataCenter().get_state()
        
        # 更新状态标签
        if state.model_class_names is None or len(state.model_class_names) == 0:
            status_label.setText("等待模型加载...")
            status_label.setStyleSheet("""
                QLabel {
                    color: #666666; 
                    font-weight: bold; 
                    font-size: 12px;
                    padding: 5px;
                    background-color: #f0f0f0;
                    border-radius: 3px;
                }
            """)
            class_list.clear()
            info_label.setText("已选择: 0 个类别")
            return
        
        # 更新状态标签
        status_label.setText(f"模型已加载: {len(state.model_class_names)} 个类别")
        status_label.setStyleSheet("""
            QLabel {
                color: #2E7D32; 
                font-weight: bold; 
                font-size: 12px;
                padding: 5px;
                background-color: #E8F5E8;
                border-radius: 3px;
                border: 1px solid #4CAF50;
            }
        """)
        
        # 更新类别列表
        if class_list.count() == 0 and state.model_class_names:
            for i, class_name in enumerate(state.model_class_names):
                item = QListWidgetItem(f"{i}: {class_name}")
                item.setData(Qt.UserRole, i)  # 存储类别ID
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                item.setCheckState(Qt.Unchecked)
                class_list.addItem(item)
        
        # 更新选中状态
        selected_ids = state.selected_class_ids if state.selected_class_ids else []
        for i in range(class_list.count()):
            item = class_list.item(i)
            class_id = item.data(Qt.UserRole)
            if class_id in selected_ids:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
        
        # 更新选择信息
        checked_count = sum(1 for i in range(class_list.count()) 
                           if class_list.item(i).checkState() == Qt.Checked)
        info_label.setText(f"已选择: {checked_count} 个类别")
    
    def on_select_all():
        """全选所有类别"""
        for i in range(class_list.count()):
            class_list.item(i).setCheckState(Qt.Checked)
        print("✅ 已选择所有类别")
    
    def on_clear_all():
        """清空所有选择"""
        for i in range(class_list.count()):
            class_list.item(i).setCheckState(Qt.Unchecked)
        print("🔄 已清空所有选择")
    
    def on_apply():
        """应用选择的类别"""
        selected_ids = []
        for i in range(class_list.count()):
            item = class_list.item(i)
            if item.checkState() == Qt.Checked:
                class_id = item.data(Qt.UserRole)
                selected_ids.append(class_id)
        
        # 更新DataCenter
        DataCenter().update_state(selected_class_ids=selected_ids)
        
        print(f"✅ 已应用选择: {len(selected_ids)} 个类别")
        print(f"选择的类别ID: {selected_ids}")
    
    # 连接按钮事件
    select_all_btn.clicked.connect(on_select_all)
    clear_all_btn.clicked.connect(on_clear_all)
    apply_btn.clicked.connect(on_apply)
    
    # 启动定时器
    update_timer.start(500)  # 每500ms更新一次
    
    # 存储引用到组件
    group.update_timer = update_timer
    group.class_list = class_list
    group.status_label = status_label
    group.info_label = info_label
    
    return group


def get_class_selector():
    """
    获取类别选择组件
    
    Returns:
        QGroupBox: 类别选择组件
    """
    return create_class_selector()
