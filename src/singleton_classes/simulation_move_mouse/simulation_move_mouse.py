"""
鼠标模拟器模块 - 单例模式
用于模拟平滑的鼠标移动，支持高频率的精确控制
适用于FPS游戏中的瞄准辅助系统
"""

import time
import threading
from pynput.mouse import Controller
from collections import deque

class MouseSimulator:
    """
    鼠标模拟器单例类
    通过多线程实现高频率的鼠标移动控制，支持平滑移动和残差累积
    使用单例模式确保全局只有一个鼠标控制实例
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """单例模式实现"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, fps=500, smoothing=0.4):
        """
        初始化鼠标模拟器（单例模式）
        
        参数:
            fps (int): 控制频率，默认500Hz，即每秒500次更新
            smoothing (float): 平滑系数，范围0-1，值越小越平滑，默认0.4
            
        注意:
            在单例模式中，参数只在第一次创建实例时生效
            后续调用时参数会被忽略，返回已存在的实例
        """
        # 防止重复初始化
        if self._initialized:
            return
            
        # 创建鼠标控制器实例
        self.mouse = Controller()
        
        # 当前速度向量（像素/秒）
        self.vx = 0  # X轴速度
        self.vy = 0  # Y轴速度
        
        # 平滑参数
        self.smoothing = smoothing  # 指数平滑系数
        
        # 控制参数
        self.fps = fps  # 更新频率
        self.running = True  # 运行状态标志
        
        # 残差累积变量，用于处理小数像素移动
        self.rx = 0  # X轴残差累积
        self.ry = 0  # Y轴残差累积
        
        # 向量执行时间控制
        self.vector_start_time = 0  # 向量开始时间
        self.max_duration = 0.05  # 最大执行时间（秒）
        self.decay_rate = 0.95  # 减速系数，每次循环速度乘以这个值

        # 位移历史记录 
        # 已经使用了maxlen参数，所以不需要再手动清理过期记录
        self.displacement_history = deque(maxlen=1000)  # 存储 (timestamp, dx, dy) 的队列
        
        # 创建并启动控制线程
        # daemon=True 确保主程序退出时线程也会退出
        self.thread = threading.Thread(target=self._driver_loop, daemon=True)
        self.thread.start()
        
        # 标记为已初始化
        self._initialized = True
        print(f"MouseSimulator 单例初始化完成，FPS: {fps}, 平滑系数: {smoothing}")

    def submit_vector(self, vx, vy):
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
        self.vx = vx
        self.vy = vy
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
        # 计算每次循环的延迟时间
        delay = 1.0 / self.fps
        
        # 平滑处理用的临时变量
        sx, sy = 0, 0
        
        # 主控制循环
        while self.running:
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
            target_sx = self.vx * delay
            target_sy = self.vy * delay

            # 步骤2: 应用指数平滑算法
            # 平滑系数越小，移动越平滑，但响应越慢
            # 正确的指数平滑：新值 = 平滑系数 * 目标值 + (1-平滑系数) * 旧值
            sx = self.smoothing * target_sx + (1 - self.smoothing) * sx
            sy = self.smoothing * target_sy + (1 - self.smoothing) * sy

            # 步骤3: 残差累积处理
            # 将小数部分累积起来，避免丢失精度
            self.rx += sx
            self.ry += sy
            
            # 步骤4: 提取整数部分作为实际移动量
            move_x = int(self.rx)
            move_y = int(self.ry)
            
            # 步骤5: 更新残差（减去已移动的整数部分）
            self.rx -= move_x
            self.ry -= move_y

            # 步骤6: 执行鼠标移动（只在需要时移动）
            if move_x != 0 or move_y != 0:
                self.mouse.move(move_x, move_y)
                # current_time = time.time()
                # self.displacement_history.append((current_time, move_x, move_y))
                

            # 步骤7: 等待下一个控制周期
            time.sleep(delay)

    def stop(self):
        """
        停止鼠标模拟器
        
        功能:
            1. 设置停止标志
            2. 等待控制线程结束
            3. 确保资源正确释放
        """
        # 设置停止标志，让控制循环退出
        self.running = False
        
        # 等待控制线程结束
        self.thread.join()
    
    # 获取位移的累计值
    def get_displacement_history(self, seconds_back=0.02):
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
        
        return total_dx, total_dy

    
    def get_status(self):
        """
        获取鼠标模拟器状态信息
        
        Returns:
            dict: 包含当前状态信息的字典
        """
        return {
            "running": self.running,
            "fps": self.fps,
            "smoothing": self.smoothing,
            "decay_rate": self.decay_rate,
            "max_duration": self.max_duration,
            "current_velocity": (self.vx, self.vy),
            "residual": (self.rx, self.ry),
            "thread_alive": self.thread.is_alive() if hasattr(self, 'thread') else False
        }
    
    def is_running(self):
        """检查模拟器是否正在运行"""
        return self.running and hasattr(self, 'thread') and self.thread.is_alive()
    
    def update_config(self, fps=None, smoothing=None):
        """
        动态更新配置参数
        
        Args:
            fps (int, optional): 新的控制频率
            smoothing (float, optional): 新的平滑系数
            
        注意:
            这个方法允许在运行时动态调整配置
            但不会重新创建线程，只是更新参数
        """
        if fps is not None:
            self.fps = fps
            print(f"✅ 更新FPS为: {fps}")
        
        if smoothing is not None:
            self.smoothing = smoothing
            print(f"✅ 更新平滑系数为: {smoothing}")
        
        if fps is None and smoothing is None:
            print("⚠️  没有提供要更新的参数")
    
    def update_decay_rate(self, decay_rate):
        """
        动态更新减速系数
        
        Args:
            decay_rate (float): 新的减速系数，范围0-1
                               值越大减速越慢，值越小减速越快
                               默认值: 0.95
        """
        if 0 < decay_rate < 1:
            self.decay_rate = decay_rate
            print(f"✅ 更新减速系数为: {decay_rate}")
        else:
            print("⚠️  减速系数必须在0-1之间")


# 便捷函数
def get_mouse_simulator(fps=500, smoothing=0.4):
    """
    获取鼠标模拟器单例实例
    
    Args:
        fps (int): 控制频率，默认500Hz
        smoothing (float): 平滑系数，默认0.4
        
    Returns:
        MouseSimulator: 鼠标模拟器单例实例
    """
    return MouseSimulator(fps, smoothing)


def get_default_mouse_simulator():
    """获取默认配置的鼠标模拟器实例"""
    return MouseSimulator()


# 测试代码
if __name__ == "__main__":
    """
    测试鼠标模拟器单例的基本功能
    演示如何使用单例模式进行平滑的鼠标移动
    """
    pass
