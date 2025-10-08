
import time
from utils.singleton.main import singleton
from pyadrc import FeedbackTF  # type: ignore
from simple_pid import PID  # type: ignore

# 小球运动
@singleton
class BallMovement:
    """小球运动"""
    def __init__(self, move_speed=4.0):
        self.move_speed = move_speed
        self.current = 0.0

        self.thread = None
        self.is_running = False
    
    # 持续移动
    def move(self):
        self.current += self.move_speed


@singleton
class ADRCController:
    """ADRC控制器"""
    def __init__(self):
        self.controller = FeedbackTF(
            order=1,        # 控制器阶数（1或2）
            delta=0.01,      # 采样时间 ⚠️ 必须匹配实际调用频率！
            b0=1.0,         # 系统增益估计
            w_cl=40.0,      # 闭环带宽
            k_eso=2.0       # 观测器带宽倍数
        )
        self.current = 0.0
    
    def control(self, error, dt):
        """error: 目标相对偏移, dt: 时间间隔"""
        return self.controller(0, error, zoh=True)
        # return self.controller(0, error, zoh=False)
    
    def move(self, output, dt):
        self.current += output * dt



def run_adrc_only():
    """只测试ADRC控制器"""
    dt = 0.01
    print("🎯 测试 ADRC 控制器")
    print("-" * 50)
    count = 0
    while ADRCController().current < 200:
        BallMovement().move()
        error = BallMovement().current - ADRCController().current
        output = ADRCController().control(error, dt)
        print(f"{count} | Ball: {BallMovement().current:.2f} | ADRC: {ADRCController().current:.2f} | Error: {(error):.2f} | Output: {output:.2f}")
        count += 1
        ADRCController().move(output, dt)
       
        time.sleep(dt)


if __name__ == "__main__":
    run_adrc_only()