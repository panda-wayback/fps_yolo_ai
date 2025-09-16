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
from singleton_classes.pid_controller.pid_controller import get_pid_res
from singleton_classes.screenshot_img.main import MouseScreenshot
from singleton_classes.simulation_move_mouse.simulation_move_mouse import MouseSimulator


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
        
        self._initialized = True
        print("🎯 TargetTracker 单例初始化完成")
    
    def start(self):
        """启动跟踪线程"""
        if self._running:
            print("⚠️ 跟踪线程已在运行")
            return
        
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        print("🎯 开始目标跟踪")
    
    def stop(self):
        """停止跟踪线程"""
        if not self._running:
            print("⚠️ 跟踪线程未在运行")
            return
        
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
                
                # 获取YOLO结果
                yolo_results = state.yolo_results
                if yolo_results != self.last_yolo_results:
                    self.last_yolo_results = yolo_results
                    self._on_yolo_results_changed(yolo_results)
                
                # 获取截图
                screenshot_img = state.screenshot_img
                if screenshot_img is not None and screenshot_img is not self.last_screenshot_img:
                    self.last_screenshot_img = screenshot_img
                    self._on_screenshot_changed(screenshot_img)
                
                # 获取鼠标位置
                mouse_pos = state.mouse_pos
                if mouse_pos:
                    self._on_mouse_pos_changed(mouse_pos)
                
                # 获取区域信息
                region = state.region
                if region:
                    self._on_region_changed(region)
                
            except Exception as e:
                print(f"❌ 跟踪循环错误: {e}")
            
            time.sleep(self._delay)
    
    def _on_yolo_results_changed(self, yolo_results):
        """YOLO结果变化处理"""
        if yolo_results:
            print(f"🎯 检测到 {len(yolo_results)} 个目标")
            # 这里可以添加目标处理逻辑
            # 获取区域信息
            region = self.data_center.get_state().region
            x_output, y_output = get_pid_res(yolo_results, region)
            # 提交PID结果
            MouseSimulator().submit_vector(-x_output, -y_output)

    
    def _on_screenshot_changed(self, screenshot_img):
        """截图变化处理"""
        print(f"📸 截图更新: {screenshot_img.shape if hasattr(screenshot_img, 'shape') else 'Unknown'}")
        # 这里可以添加图像处理逻辑
    
    def _on_mouse_pos_changed(self, mouse_pos):
        """鼠标位置变化处理"""
        print(f"🖱️ 鼠标位置: {mouse_pos}")
        # 这里可以添加鼠标位置处理逻辑

        # 更新鼠标位置配置 用于截图
        MouseScreenshot().update_config(mouse_pos=mouse_pos)
    
    def _on_region_changed(self, region):
        """区域变化处理"""
        print(f"📐 区域更新: {region}")
        # 这里可以添加区域处理逻辑

        # 更新区域配置 用于截图
        MouseScreenshot().update_config(region=region)
    
    def set_fps(self, fps):
        """设置处理频率"""
        self.fps = max(10, min(120, fps))
        self._delay = 1.0 / self.fps
        print(f"✅ 设置处理频率: {self.fps} FPS")
    
    def get_status(self):
        """获取状态信息"""
        return {
            'running': self._running,
            'fps': self.fps,
            'thread_alive': self._thread.is_alive() if self._thread else False,
            'last_yolo_count': len(self.last_yolo_results) if self.last_yolo_results else 0,
            'has_screenshot': self.last_screenshot_img is not None
        }


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