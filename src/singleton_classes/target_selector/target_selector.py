#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
目标选择器 - 简洁版
从DataCenter获取数据并处理目标选择
"""

import time
import threading
from threading import Lock
from singleton_classes.data_center import DataCenter, get_data_center
from utils.yolo.yolo_result_utils import select_best_target


class TargetSelector:
    """目标选择器单例类"""
    
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
            
        self.data_center = DataCenter()
        self._running = False
        self._thread = None
        
        # 目标数据
        self.current_target = None
        self.reference_vector = None
        
        # 处理频率
        self.fps = 1000
        self._delay = 1.0 / self.fps
        
        self._initialized = True
        print("🎯 TargetSelector 单例初始化完成")
    
    def start(self):
        """启动目标选择线程"""
        if self._running:
            print("⚠️ 目标选择线程已在运行")
            return
        
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        print("🎯 开始目标选择")
    
    def stop(self):
        """停止目标选择线程"""
        if not self._running:
            print("⚠️ 目标选择线程未在运行")
            return
        
        self._running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1)
        print("🛑 停止目标选择")
    
    def _loop(self):
        """主循环线程"""
        last_yolo_results = None
        while self._running:
            try:
                # 获取DataCenter状态
                state = self.data_center.get_state()
                # print(f"🎯 目标选择循环: {id(last_yolo_results)} != {id(state.yolo_results)}  {state.yolo_results}")
                
                # 处理YOLO结果
                if id(last_yolo_results) != id(state.yolo_results):
                    last_yolo_results = state.yolo_results
                    self._process_yolo_results(state.yolo_results)
                
                
            except Exception as e:
                print(f"❌ 目标选择循环错误: {e} ")
            
            time.sleep(self._delay)
    
    
    def _process_yolo_results(self, yolo_results):
        """处理YOLO检测结果"""
        if yolo_results is None:
            print("🎯 处理YOLO结果: 无结果")
            self.current_target = None
            return
            
        print(f"🎯 处理YOLO结果: {len(yolo_results)} 个目标")
        if yolo_results is None:
            print("🎯 处理YOLO结果: 无结果")
            self.current_target = None
            return
        
        print(f"🎯 参考向量: {self.data_center.get_state().region}")

        screen_center = (
            self.data_center.get_state().region[0] /  2 ,
            self.data_center.get_state().region[1] / 2
        )
        print(f"🎯 屏幕中心: {screen_center}")
        class_ids = DataCenter().get_state().model_class_ids
        best_target = select_best_target(
            yolo_results = yolo_results,
            screen_center = screen_center,
            reference_vector = self.reference_vector,
            class_ids = class_ids
            )
        
        self.current_target = best_target
        self.reference_vector = self.current_target["vector"]
        
        print(f"🎯 选择目标: {self.reference_vector}")

        get_data_center().update_state(best_target=best_target)

        print(f"✅ 选择目标: {self.current_target}")
    
    
    def get_current_target(self):
        """获取当前目标"""
        return self.current_target
    
    def get_status(self):
        """获取状态信息"""
        return {
            "running": self._running,
            "fps": self.fps,
            "has_target": self.current_target is not None,
            "target_type": self.current_target.get("type") if self.current_target else None,
            "thread_alive": self._thread.is_alive() if self._thread else False
        }
    
    def set_fps(self, fps):
        """设置处理频率"""
        self.fps = max(10, min(120, fps))
        self._delay = 1.0 / self.fps
        print(f"✅ 设置处理频率: {self.fps} FPS")
    
    def clear_target(self):
        """清除当前目标"""
        self.current_target = None
        self.reference_vector = None
        print("🔄 已清除目标")


if __name__ == "__main__":
    # 测试代码
    print("=== TargetSelector 测试 ===")
    
    selector = TargetSelector()
    
    # 启动线程
    selector.start()
    
    # 运行一段时间
    time.sleep(3)
    
    # 检查状态
    status = selector.get_status()
    print(f"状态: {status}")
    
    # 停止线程
    selector.stop()
