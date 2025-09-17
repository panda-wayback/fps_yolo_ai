#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模型类别选择组件 - 简洁版
"""

from PySide6.QtWidgets import (QHBoxLayout, QPushButton, QLabel, 
                               QListWidget, QListWidgetItem)
from PySide6.QtCore import Qt
from pyside.UI.basic.basic_layout import create_vertical_card
from singleton_classes.data_center import DataCenter


def create_class_selector():
    """创建简洁的类别选择组件"""
    group = create_vertical_card("类别选择")
    layout = group._layout
    
    # 状态标签
    status_label = QLabel("等待模型加载...")
    status_label.setStyleSheet("color: #333; font-weight: bold; padding: 5px; background: #f0f0f0; border-radius: 3px;")
    layout.addWidget(status_label)
    
    # 类别列表
    class_list = QListWidget()
    class_list.setMaximumHeight(120)
    class_list.setMinimumHeight(80)
    class_list.setStyleSheet("border: 1px solid #ccc; border-radius: 3px;")
    layout.addWidget(class_list)
    
    # 按钮
    refresh_btn = QPushButton("刷新")
    select_btn = QPushButton("全选")
    clear_btn = QPushButton("清空")
    apply_btn = QPushButton("应用")
    
    refresh_btn.setStyleSheet("QPushButton { background: #FF9800; color: white; }")
    select_btn.setStyleSheet("QPushButton { background: #4CAF50; color: white; }")
    clear_btn.setStyleSheet("QPushButton { background: #f44336; color: white; }")
    apply_btn.setStyleSheet("QPushButton { background: #2196F3; color: white; }")
    
    btn_layout = QHBoxLayout()
    btn_layout.addWidget(refresh_btn)
    btn_layout.addWidget(select_btn)
    btn_layout.addWidget(clear_btn)
    btn_layout.addWidget(apply_btn)
    layout.addLayout(btn_layout)
    
    # 信息标签
    info_label = QLabel("已选择: 0 个类别")
    info_label.setStyleSheet("color: #666; font-size: 11px; padding: 3px;")
    layout.addWidget(info_label)
    
    def refresh_data():
        """刷新数据 - 获取现在的类别列表和选择状态"""
        state = DataCenter().get_state()
        
        if not state.model_class_names:
            status_label.setText("等待模型加载...")
            status_label.setStyleSheet("color: #333; font-weight: bold; padding: 5px; background: #f0f0f0; border-radius: 3px;")
            class_list.clear()
            info_label.setText("已选择: 0 个类别")
            return
        
        # 模型已加载
        status_label.setText(f"模型已加载: {len(state.model_class_names)} 个类别")
        status_label.setStyleSheet("color: #2E7D32; font-weight: bold; padding: 5px; background: #E8F5E8; border-radius: 3px; border: 1px solid #4CAF50;")
        
        # 清空并重新填充列表
        class_list.clear()
        for i, name in enumerate(state.model_class_names):
            item = QListWidgetItem(f"{i}: {name}")
            item.setData(Qt.UserRole, i)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            class_list.addItem(item)
        
        # 根据DataCenter的selected_class_ids设置选中状态
        selected_ids = state.selected_class_ids or []
        for i in range(class_list.count()):
            item = class_list.item(i)
            class_id = item.data(Qt.UserRole)
            item.setCheckState(Qt.Checked if class_id in selected_ids else Qt.Unchecked)
        
        # 更新计数
        update_count()
        print(f"✅ 已刷新类别列表: {len(state.model_class_names)} 个类别")
    
    def update_count():
        """更新选择计数"""
        checked_count = sum(1 for i in range(class_list.count()) 
                           if class_list.item(i).checkState() == Qt.Checked)
        info_label.setText(f"已选择: {checked_count} 个类别")
    
    def on_select_all():
        """全选"""
        for i in range(class_list.count()):
            class_list.item(i).setCheckState(Qt.Checked)
        update_count()
        print("✅ 已选择所有类别")
    
    def on_clear_all():
        """清空"""
        for i in range(class_list.count()):
            class_list.item(i).setCheckState(Qt.Unchecked)
        update_count()
        print("🔄 已清空所有选择")
    
    def on_apply():
        """应用选择 - 将最新的数据更新到DataCenter"""
        selected_ids = []
        for i in range(class_list.count()):
            item = class_list.item(i)
            if item.checkState() == Qt.Checked:
                selected_ids.append(item.data(Qt.UserRole))
        
        DataCenter().update_state(selected_class_ids=selected_ids)
        print(f"✅ 已应用选择: {len(selected_ids)} 个类别")
        print(f"选择的类别ID: {selected_ids}")
    
    # 连接事件
    refresh_btn.clicked.connect(refresh_data)
    select_btn.clicked.connect(on_select_all)
    clear_btn.clicked.connect(on_clear_all)
    apply_btn.clicked.connect(on_apply)
    
    # 监听列表变化，实时更新计数
    class_list.itemChanged.connect(update_count)
    
    # 存储引用
    group.class_list = class_list
    group.status_label = status_label
    group.info_label = info_label
    group.refresh_data = refresh_data  # 暴露刷新方法
    
    return group


def get_class_selector():
    """获取类别选择组件"""
    return create_class_selector()
