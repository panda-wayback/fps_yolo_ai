"""
鼠标模拟器模块 - 单例模式
用于模拟平滑的鼠标移动，支持高频率的精确控制
适用于FPS游戏中的瞄准辅助系统
"""

import time
import threading
from collections import deque
from typing import Tuple
from pynput.mouse import Controller

from utils.singleton.main import singleton


@singleton
class MouseSimulator:
    """
    鼠标模拟器单例类
    通过多线程实现高频率的鼠标移动控制，支持平滑移动和残差累积
    使用单例模式确保全局只有一个鼠标控制实例
    """
    
    def __init__(self, fps=1000, smoothing=0.4):
        """
        初始化鼠标模拟器（单例模式）
        
        参数:
            fps (int): 控制频率，默认500Hz，即每秒500次更新
            smoothing (float): 平滑系数，范围0-1，值越小越平滑，默认0.4
            
        注意:
            在单例模式中，参数只在第一次创建实例时生效
            后续调用时参数会被忽略，返回已存在的实例
        """
        import platform
        if platform.system() == "Windows":

            from utils.move_mouse.windows_mouse_controller import WindowsMouseController
            self.mouse = WindowsMouseController()
        else:
            self.mouse = Controller()
        # 向量执行时间控制
        self.vector_start_time = 0  # 向量开始时间

        self.vx = 0  # 向量X轴速度
        self.vy = 0  # 向量Y轴速度

        self.fps = 1000
        self.smoothing = 0.4
        self.max_duration = 0.05
        self.decay_rate = 0.95
        self.delay = 1.0 / self.fps

        # 位移历史记录 
        self.displacement_history = deque(maxlen=1000)  # 存储 (timestamp, dx, dy) 的队列
        self.thread = None
        self.is_running = False
    
    # 修改配置
    def update_config(self, 
        fps=None, # 更新频率
        smoothing=None, # 平滑系数
        max_duration=None, # 最大执行时间
        decay_rate=None, # 减速系数
    ):
        """
        修改配置
        """
        if fps is not None:
            self.fps = fps
        if smoothing is not None:
            self.smoothing = smoothing
        if max_duration is not None:
            self.max_duration = max_duration
        if decay_rate is not None:
            self.decay_rate = decay_rate
        print(f"✅ 更新FPS为: {fps}, 平滑系数: {smoothing}")
        if fps is None and smoothing is None:
            print("⚠️  没有提供要更新的参数")

    def submit_vector(self,vector: tuple[float, float]):
        """
        提交新的速度向量
        
        参数:
            vx (float): X轴速度，单位：像素/秒
            vy (float): Y轴速度，单位：像素/秒
            
        说明:
            这个方法会立即更新当前的速度向量
            速度向量会在下一个控制循环中被应用
            每个向量最多执行0.1秒
        """

        self.vx = vector[0]
        self.vy = vector[1]
        # print(f"✅ 提交新的速度向量: vx={vector[0]}, vy={vector[1]}")
        self.vector_start_time = time.time()  # 记录开始时间

    def _driver_loop(self):
        """
        主控制循环（在独立线程中运行）
        
        功能:
            1. 以指定频率持续更新鼠标位置
            2. 应用平滑算法减少抖动
            3. 使用残差累积确保精确的像素级移动
            4. 只在实际需要移动时才调用鼠标API
        """
        # 残差累积变量，用于处理小数像素移动
        error_x = 0  # X轴残差累积
        error_y = 0  # Y轴残差累积
        
        # 平滑处理用的临时变量
        sx, sy = 0, 0
        
        # 主控制循环
        while self.is_running:
            # print(f"✅ 正在移动鼠标: vx={self.vx}, vy={self.vy}")
            # 检查向量执行时间是否超过最大持续时间
            if time.time() - self.vector_start_time > self.max_duration:
                # 平滑减速而不是突然归0
                self.vx *= self.decay_rate
                self.vy *= self.decay_rate
                
                # 当速度很小时，直接设为0避免无限接近0
                if abs(self.vx) < 0.1:
                    self.vx = 0
                if abs(self.vy) < 0.1:
                    self.vy = 0
            
            # 步骤1: 根据当前速度计算本次移动量
            # 将速度(像素/秒)转换为单次移动量(像素)
            target_sx = self.vx * self.delay
            target_sy = self.vy * self.delay

            # # 步骤2: 应用指数平滑算法
            # # 平滑系数越小，移动越平滑，但响应越慢
            # # 正确的指数平滑：新值 = 平滑系数 * 目标值 + (1-平滑系数) * 旧值
            # sx = self.smoothing * target_sx + (1 - self.smoothing) * sx
            # sy = self.smoothing * target_sy + (1 - self.smoothing) * sy

            # 步骤3: 残差累积处理
            # 将小数部分累积起来，避免丢失精度
            error_x += target_sx
            error_y += target_sy
            
            # 步骤4: 提取整数部分作为实际移动量
            move_x = int(error_x)
            move_y = int(error_y)
            
            # 步骤5: 更新残差（减去已移动的整数部分）
            error_x -= move_x
            error_y -= move_y

            # 步骤6: 执行鼠标移动（只在需要时移动）
            if move_x != 0 or move_y != 0:
                self.mouse.move(move_x, move_y)
                self.record_displacement(move_x, move_y)

            # 步骤7: 等待下一个控制周期
            time.sleep(self.delay)
    # 记录位移
    def record_displacement(self, move_x, move_y):
        """
        记录位移
        """
        current_time = time.time()
        self.displacement_history.append((current_time, move_x, move_y))

    # 开始移动
    def run(self):
        """
        开始移动
        """
        if self.is_running:
            self.stop()
            time.sleep(0.1)
        self.is_running = True
        self.thread = threading.Thread(target=self._driver_loop, daemon=True)
        self.thread.start()
    
    def stop(self):
        """
        停止移动
        """
        self.is_running = False
        if self.thread is not None:
            self.thread.join()
            self.thread = None
    
    # 获取位移的累计值
    def get_displacement_history(self, seconds_back=0.02) -> Tuple[float, float]:
        """
        获取位移的累计值
        """
        current_time = time.time()
        cutoff_time = current_time - seconds_back

        # 计算累计值
        total_dx = 0
        total_dy = 0
        for timestamp, dx, dy in self.displacement_history:
            if timestamp > cutoff_time:
                total_dx += dx
                total_dy += dy
        
        return (total_dx, total_dy)


mouse_simulator = MouseSimulator()

# 便捷函数
def get_mouse_simulator():
    """
    获取鼠标模拟器单例实例
    """
    return mouse_simulator



# 测试代码
if __name__ == "__main__":
    """
    测试鼠标模拟器单例的基本功能
    演示如何使用单例模式进行平滑的鼠标移动
    """
    pass
