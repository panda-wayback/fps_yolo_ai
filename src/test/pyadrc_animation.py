
import time
import threading
from utils.singleton.main import singleton
from pyadrc import FeedbackTF  # type: ignore

# 小球运动
@singleton
class BallMovement:
    """小球运动 - 1000Hz高频线程更新"""
    def __init__(self, move_speed=4200.0):
        """
        move_speed: 每秒的移动速度（单位/秒）
        """
        self.move_speed = move_speed  # 每秒移动的距离
        self.current = 0.0
        
        self.thread = None
        self.is_running = False
        self.update_frequency = 1000  # Hz
        self.dt = 1.0 / self.update_frequency  # 0.001秒
    
    def _move_loop(self):
        """线程循环：1000Hz频率更新位置"""
        while self.is_running:
            # 每次移动 = 速度 × 时间间隔
            self.current += self.move_speed * self.dt
            time.sleep(self.dt)
    
    def start(self):
        """启动移动线程"""
        if self.is_running:
            print("⚠️ 小球已在运行")
            return
        
        self.is_running = True
        self.thread = threading.Thread(target=self._move_loop, daemon=True)
        self.thread.start()
        print(f"✅ 小球开始移动 (速度: {self.move_speed} 单位/秒, 频率: {self.update_frequency}Hz)")
    
    def stop(self):
        """停止移动线程"""
        if not self.is_running:
            return
        
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=1.0)
        print("🛑 小球停止移动")
    
    def reset(self):
        """重置位置"""
        self.current = 0.0


@singleton
class ADRCController:
    """ADRC控制器"""
    def __init__(self):
        self.controller = FeedbackTF(
            order=1,        # 控制器阶数（1或2）
            delta=0.01,      # 采样时间 ⚠️ 必须匹配实际调用频率！
            b0=0.8,         # 系统增益估计 - 实际系统：输入x*dt = 位移
            w_cl=100.0,      # 闭环带宽 [rad/s] - 稳定时间≈0.067s，增大提高响应速度
            k_eso=2.5       # 观测器带宽倍数 - 2-3范围最佳，太高会放大噪声
        )
        self.current = 0.0
    
    def control(self, error, dt):
        """error: 目标相对偏移, dt: 时间间隔"""
        return self.controller(0, error, zoh=True)
        # return self.controller(0, error, zoh=False)
    
    def move(self, output, dt):
        self.current += output * dt



def run_adrc_only():
    """测试ADRC控制器跟踪高频移动的目标"""
    dt = 0.001  # 控制器更新频率：100Hz
    
    print("=" * 70)
    print("🎯 ADRC跟踪高频移动目标测试")
    print("=" * 70)
    print(f"小球：{BallMovement().move_speed} 单位/秒，更新频率 1000Hz")
    print(f"控制器：更新频率 {1/dt:.0f}Hz (delta={ADRCController().controller.delta})")
    print("-" * 70)
    
    # 启动小球移动线程
    BallMovement().start()
    
    try:
        print(f"\n{'Time(s)':<8} | {'Ball':<8} | {'ADRC':<8} | {'Error':<8} | {'Output':<8}")
        print("-" * 60)
        
        start_time = time.time()
        last_print_time = start_time
        test_duration = 1.0  # 监控10秒
        
        while time.time() - start_time < test_duration:
            # 获取当前误差（小球在独立线程中持续移动）
            error = BallMovement().current - ADRCController().current
            
            # 控制器计算输出
            output = ADRCController().control(error, dt)
            
            # 应用控制输出
            ADRCController().move(output, dt)
            
            # 每0.1秒打印一次
            current_time = time.time()
            if current_time - last_print_time >= 0.01:
                elapsed = current_time - start_time
                print(f"{elapsed:<8.2f} | {BallMovement().current:<8.2f} | "
                      f"{ADRCController().current:<8.2f} | {error:<8.2f} | {output:<8.2f}")
                last_print_time = current_time
            
            # 控制器以100Hz运行
            time.sleep(dt)
            
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断")
    finally:
        # 停止小球移动
        BallMovement().stop()
        
        # 打印统计
        print("\n" + "=" * 70)
        print("📊 测试结果")
        print("=" * 70)
        print(f"小球最终位置: {BallMovement().current:.2f}")
        print(f"ADRC最终位置: {ADRCController().current:.2f}")
        print(f"最终误差: {abs(BallMovement().current - ADRCController().current):.2f}")


if __name__ == "__main__":
    run_adrc_only()