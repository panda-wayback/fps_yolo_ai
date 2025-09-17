#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
目标跟踪器单例类
不断获取DataCenter中的变量并处理
"""

import time
import threading
from threading import Lock
from singleton_classes.data_center import DataCenter
from singleton_classes.target_selector.target_selector import TargetSelector


class TargetTracker:
    """目标跟踪器单例类"""
    
    _instance = None
    _lock = Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        # 数据源
        self.data_center = DataCenter()
        
        # 线程控制
        self._running = False
        self._thread = None
        
        # 处理频率
        self.fps = 60
        self._delay = 1.0 / self.fps
        
        # 状态变量
        self.last_yolo_results = None
        self.last_screenshot_img = None
        
        # 目标选择器
        self.target_selector = TargetSelector()
        
        self._initialized = True
        print("🎯 TargetTracker 单例初始化完成")
    
    def start(self):
        """启动跟踪线程"""
        if self._running:
            print("⚠️ 跟踪线程已在运行")
            return
        
        # 启动目标选择器
        self.target_selector.start()
        
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        print("🎯 开始目标跟踪")
    
    def stop(self):
        """停止跟踪线程"""
        if not self._running:
            print("⚠️ 跟踪线程未在运行")
            return
        
        # 停止目标选择器
        self.target_selector.stop()
        
        self._running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1)
        print("🛑 停止目标跟踪")
    
    def _loop(self):
        """主循环线程"""
        while self._running:
            try:
                # 获取DataCenter状态
                state = self.data_center.get_state()
                
                # 简单的状态监控
                if state.yolo_results:
                    print(f"🎯 检测到 {len(state.yolo_results)} 个目标")
                
                if state.screenshot_img is not None:
                    print("📸 截图更新")
                
                if state.mouse_pos:
                    print(f"🖱️ 鼠标位置: {state.mouse_pos}")
                
            except Exception as e:
                print(f"❌ 跟踪循环错误: {e}")
            
            time.sleep(self._delay)
    
    
    
    def set_fps(self, fps):
        """设置处理频率"""
        self.fps = max(10, min(120, fps))
        self._delay = 1.0 / self.fps
        print(f"✅ 设置处理频率: {self.fps} FPS")
    
    def get_status(self):
        """获取状态信息"""
        target_status = self.target_selector.get_status()
        return {
            'running': self._running,
            'fps': self.fps,
            'thread_alive': self._thread.is_alive() if self._thread else False,
            'target_selector': target_status
        }
    
    def clear_target(self):
        """清除当前目标"""
        self.target_selector.clear_target()
    
    def get_current_target(self):
        """获取当前目标"""
        return self.target_selector.get_current_target()


# 便捷函数
def get_target_tracker():
    """获取目标跟踪器单例"""
    return TargetTracker()

def start_tracking():
    """启动跟踪"""
    tracker = get_target_tracker()
    tracker.start()
    return tracker

def stop_tracking():
    """停止跟踪"""
    tracker = get_target_tracker()
    tracker.stop()