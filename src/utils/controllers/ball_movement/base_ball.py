"""
小球运动模拟器 - 用于测试控制器
支持动态提交速度
"""

import time
import threading

from utils.controllers.adrc.ladrc import LADRCController

class BallMovement:
    """
    小球运动模拟器（单例模式）
    支持动态提交速度，用于测试控制器性能
    """
    
    def __init__(self):
        """初始化小球"""
        self.current = 0.0  # 当前位置
        self.move_speed = 0.0  # 移动速度（单位/秒）
        
        self.fps = 1000
        self.smoothing = 0.8
        self.max_duration = 0.1
        self.delay = 1.0 / self.fps
        
        
        # 速度向量提交时间
        self.vector_start_time = 0
        
        # 线程控制
        self.thread = None
        self.is_running = False

    
    def submit_vector(self, speed: float):
        """
        提交速度向量
        
        Args:
            speed: 移动速度，单位：单位/秒
        """
        self.move_speed = speed
        self.vector_start_time = time.time()
    
    def _driver_loop(self):
        """移动循环（运行在独立线程）"""
        # 平滑速度
        # Sₜ = α * Xₜ + (1 - α) * Sₜ₋₁
        sx = 0
        while self.is_running:
            # 检查向量执行时间是否超过最大持续时间
            if time.time() - self.vector_start_time > self.max_duration:
                self.move_speed = 0
                
            # 当速度很小时，直接设为0避免无限接近0
            if abs(self.move_speed) < 1:
                self.move_speed = 0
            

            x = self.move_speed * self.delay
            sx_next = self.smoothing * x + (1 - self.smoothing) * sx

            # 更新位置：位置 += 速度 × 时间
            self.current += sx_next
            sx = sx_next
            # 等待下一个控制周期
            time.sleep(self.delay)
    
    def start(self):
        """启动小球运动线程"""
        self.stop()
        time.sleep(0.1)
        self.is_running = True
        self.thread = threading.Thread(target=self._driver_loop, daemon=True)
        self.thread.start()
        print(f"✅ 小球运动线程已启动 (频率: {self.fps}Hz)")
    
    def stop(self):
        """停止小球运动线程"""
        if not self.is_running:
            return
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=1.0)
            self.thread = None
        print("🛑 小球运动线程已停止")
    
    def reset(self):
        """重置位置和速度"""
        self.current = 0.0
        self.move_speed = 0.0

def test1():
    ball1 = BallMovement()
    ball1.start()
    ball1_speed = 1200
    ball2 = BallMovement()
    ball2.start()
    controller = LADRCController(
        w_cl = 60,
        k_eso= 2.55,
    )
    dt = 0.045
    start_time = time.time()
    test_duration = 0.6  # 监控10秒
    count = 0
    # ball1.submit_vector(ball1_speed)
    # time.sleep(dt)
    while time.time() - start_time < test_duration:
        count += dt
        error = ball1.current - ball2.current
        output = controller.compute(error)
        print(f"{count:.2f} | ball1.current: {ball1.current:.1f} | ball2.current: {ball2.current:.1f} | error: {error:.1f} | output: {output:.1f}")
        ball2.submit_vector(output)
        ball1.submit_vector(ball1_speed)
        # 控制器以100Hz运行
        time.sleep(dt)

    pass

if __name__ == "__main__":
    test1()