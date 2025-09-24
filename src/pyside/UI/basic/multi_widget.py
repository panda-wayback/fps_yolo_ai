#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多组件添加工具
提供便捷的方法来一次性添加多个组件到布局中
"""

from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout
from typing import List, Any


def add_widgets(layout, *widgets):
    """
    向布局中添加多个组件
    
    Args:
        layout: 目标布局 (QVBoxLayout, QHBoxLayout, QGridLayout)
        *widgets: 要添加的组件列表
    
    Example:
        add_widgets(vertical_layout, widget1, widget2, widget3)
        add_widgets(horizontal_layout, *widget_list)
    """
    for widget in widgets:
        if widget is not None:
            layout.addWidget(widget)


def add_widgets_to_vertical(*widgets) -> QVBoxLayout:
    """
    创建垂直布局并添加多个组件
    
    Args:
        *widgets: 要添加的组件列表
        
    Returns:
        QVBoxLayout: 包含所有组件的垂直布局
        
    Example:
        layout = add_widgets_to_vertical(widget1, widget2, widget3)
    """
    layout = QVBoxLayout()
    add_widgets(layout, *widgets)
    return layout


def add_widgets_to_horizontal(*widgets) -> QHBoxLayout:
    """
    创建水平布局并添加多个组件
    
    Args:
        *widgets: 要添加的组件列表
        
    Returns:
        QHBoxLayout: 包含所有组件的水平布局
        
    Example:
        layout = add_widgets_to_horizontal(widget1, widget2, widget3)
    """
    layout = QHBoxLayout()
    add_widgets(layout, *widgets)
    return layout


def add_widgets_to_grid(widgets: List[List[Any]], 
                       row_stretch: List[int] = None,
                       col_stretch: List[int] = None) -> QGridLayout:
    """
    创建网格布局并添加多个组件
    
    Args:
        widgets: 二维列表，每个子列表代表一行
        row_stretch: 行拉伸比例列表
        col_stretch: 列拉伸比例列表
        
    Returns:
        QGridLayout: 包含所有组件的网格布局
        
    Example:
        widgets = [
            [widget1, widget2],
            [widget3, widget4]
        ]
        layout = add_widgets_to_grid(widgets)
    """
    layout = QGridLayout()
    
    for row, row_widgets in enumerate(widgets):
        for col, widget in enumerate(row_widgets):
            if widget is not None:
                layout.addWidget(widget, row, col)
    
    # 设置行拉伸
    if row_stretch:
        for i, stretch in enumerate(row_stretch):
            layout.setRowStretch(i, stretch)
    
    # 设置列拉伸
    if col_stretch:
        for i, stretch in enumerate(col_stretch):
            layout.setColumnStretch(i, stretch)
    
    return layout


def add_layouts(layout, *layouts):
    """
    向布局中添加多个子布局
    
    Args:
        layout: 目标布局
        *layouts: 要添加的子布局列表
        
    Example:
        add_layouts(main_layout, layout1, layout2, layout3)
    """
    for sub_layout in layouts:
        if sub_layout is not None:
            layout.addLayout(sub_layout)


def create_column_layout(*widgets) -> QVBoxLayout:
    """
    创建列布局的便捷方法
    
    Args:
        *widgets: 要添加的组件列表
        
    Returns:
        QVBoxLayout: 包含所有组件的列布局
    """
    return add_widgets_to_vertical(*widgets)


def create_row_layout(*widgets) -> QHBoxLayout:
    """
    创建行布局的便捷方法
    
    Args:
        *widgets: 要添加的组件列表
        
    Returns:
        QHBoxLayout: 包含所有组件的行布局
    """
    return add_widgets_to_horizontal(*widgets)
