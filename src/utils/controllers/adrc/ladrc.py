"""
LADRC - Linear Active Disturbance Rejection Control
线性自抗扰控制器

基于 pyadrc 库的封装，提供易用的 LADRC 控制器接口。

核心思想：
1. 扩张状态观测器 (ESO) - 实时估计系统状态和"总扰动"
2. 扰动补偿 - 主动抵消扰动的影响
3. 状态反馈控制 - 实现期望的动态性能

优势：
- 对模型不确定性鲁棒
- 自动补偿各种扰动
- 参数调节简单（主要是 w_cl 和 k_eso）
- 适应不同速度范围（高速/低速）

Author: Your Name
Date: 2025-10-09
"""

from pyadrc import FeedbackTF  # type: ignore
from typing import Optional, Tuple


class LADRCController:
    """
    LADRC 控制器 - 用于位置跟踪控制
    
    适用场景：
    - 鼠标位置控制
    - 目标跟踪
    - 伺服控制
    - 任何需要快速、准确跟踪目标的场景
    
    Examples:
        >>> # 创建控制器（100Hz 控制频率）
        >>> controller = LADRCController(
        ...     order=1,
        ...     sample_time=0.01,
        ...     b0=1.0,
        ...     w_cl=60.0,
        ...     k_eso=2.5
        ... )
        >>> 
        >>> # 控制循环
        >>> dt = 0.01
        >>> while running:
        ...     error = target_position - current_position
        ...     output = controller.compute(error)
        ...     current_position += output * dt  # 应用控制输出
        ...     time.sleep(dt)
    """
    
    def __init__(
        self,
        order: int = 1,
        sample_time: float = 0.01,
        b0: float = 0.5,
        w_cl: float = 10.0,
        k_eso: float = 2.5,
        output_limits: Optional[Tuple[float, float]] = (-2000, 2000),
        rate_limits: Optional[Tuple[float, float]] = None
    ):
        """
        初始化 LADRC 控制器
        
        Parameters:
            order: int, default=1
                控制器阶数
                - 1: 一阶系统（位置控制），稳定时间 ≈ 4/w_cl 秒
                - 2: 二阶系统（位置+速度控制），稳定时间 ≈ 6/w_cl 秒
                推荐：大多数情况用 1 即可
            
            sample_time: float, default=0.01
                采样时间（秒），即控制器更新周期
                ⚠️ 必须与实际调用频率严格匹配！
                - 0.001 = 1000Hz
                - 0.01  = 100Hz
                - 0.02  = 50Hz
            
            b0: float, default=1.0
                系统增益估计
                含义：控制输出对系统的影响系数
                如果系统模型是: position += output * b0 * dt
                则设置 b0 为该系数值
                调整建议：
                - 跟踪慢、误差大 → 减小 b0 (如 0.8)
                - 超调、震荡 → 增大 b0 (如 1.2)
            
            w_cl: float, default=60.0
                闭环带宽 [rad/s] - 🎯 最重要的调节参数
                决定系统响应速度
                稳定时间 ≈ 4/w_cl 秒（一阶）或 6/w_cl 秒（二阶）
                调整建议：
                - 响应太慢 → 增大 (如 80-100)
                - 震荡不稳 → 减小 (如 40-50)
                - 推荐范围: 40-80 rad/s
            
            k_eso: float, default=2.5
                观测器带宽倍数
                观测器带宽 = k_eso × w_cl
                决定扰动估计的速度（不是主要响应速度！）
                
                ⚠️ 重要提示：
                - 如果跟踪太慢、追不上目标 → 应该增大 w_cl，而不是 k_eso！
                - k_eso 只影响对扰动的反应速度
                
                调整建议：
                - 对扰动反应慢 → 增大 (如 3.0-3.5)
                - 对噪声敏感、抖动 → 减小 (如 2.0)
                - 推荐范围: 2.0-3.0
                - ⚠️ 不要超过 4.0
            
            output_limits: Optional[Tuple[float, float]], default=(-4000, 4000)
                输出幅值限制 (min, max)
                默认限制在 -4000 到 4000 之间
            
            rate_limits: Optional[Tuple[float, float]], default=None
                输出变化率限制 (min_rate, max_rate)
                例如: (-500, 500) 限制输出每次最多变化 500
        
        Raises:
            AssertionError: 如果 order 不是 1 或 2
        """
        assert order in [1, 2], "order 必须是 1 或 2"
        assert sample_time > 0, "sample_time 必须大于 0"
        assert b0 > 0, "b0 必须大于 0"
        assert w_cl > 0, "w_cl 必须大于 0"
        assert k_eso > 0, "k_eso 必须大于 0"
        
        self.order = order
        self.sample_time = sample_time
        self.b0 = b0
        self.w_cl = w_cl
        self.k_eso = k_eso
        self.output_limits = output_limits
        self.rate_limits = rate_limits
        
        # 转换限制格式
        m_lim = output_limits if output_limits else (None, None)
        r_lim = rate_limits if rate_limits else (None, None)
        
        # 创建底层 LADRC 控制器
        self.controller = FeedbackTF(
            order=order,
            delta=sample_time,
            b0=b0,
            w_cl=w_cl,
            k_eso=k_eso,
            m_lim=m_lim,
            r_lim=r_lim
        )
        
        # 计算理论稳定时间
        if order == 1:
            self.settling_time = 4.0 / w_cl
        else:
            self.settling_time = 6.0 / w_cl
    
    def compute(self, error: float, use_zoh: bool = True) -> float:
        """
        计算控制输出
        
        Parameters:
            error: float
                误差值 = 目标值 - 当前值
                例如: target_position - current_position
            
            use_zoh: bool, default=True
                是否使用零阶保持器（Zero-Order Hold）
                True: 更稳定，推荐
                False: 理论上稍快，但可能不稳定
        
        Returns:
            float: 控制输出
                应用方式: current_value += output * dt
        
        Examples:
            >>> error = target - current
            >>> output = controller.compute(error)
            >>> current += output * dt
        """
        # 调用底层控制器
        # 第一个参数是期望值（setpoint），在误差控制中设为 0
        # 第二个参数是误差（相当于测量值）
        return self.controller(0, error, zoh=use_zoh)
    
    def reset(self):
        """
        重置控制器状态
        
        清空观测器状态和历史数据，用于：
        - 开始新的控制任务
        - 目标发生大幅跳变
        - 系统重启
        """
        # 重新创建控制器实例
        m_lim = self.output_limits if self.output_limits else (None, None)
        r_lim = self.rate_limits if self.rate_limits else (None, None)
        
        self.controller = FeedbackTF(
            order=self.order,
            delta=self.sample_time,
            b0=self.b0,
            w_cl=self.w_cl,
            k_eso=self.k_eso,
            m_lim=m_lim,
            r_lim=r_lim
        )

    def set_config(self, 
        order: Optional[int] = None, 
        sample_time: Optional[float] = None, 
        b0: Optional[float] = None, 
        w_cl: Optional[float] = None, 
        k_eso: Optional[float] = None,
        output_limits: Optional[Tuple[float, float]] = ...,  # 使用...作为哨兵值
        rate_limits: Optional[Tuple[float, float]] = ...):   # 使用...作为哨兵值
        """
        设置控制器参数 - 只修改传入的参数，未传入的参数保持原值
        
        Args:
            order: 控制器阶数 (1 或 2)，不传则保持原值
            sample_time: 采样时间（秒），不传则保持原值
            b0: 控制增益，不传则保持原值
            w_cl: 控制器带宽，不传则保持原值
            k_eso: ESO增益，不传则保持原值
            output_limits: 输出限幅 (min, max)，不传则保持原值
            rate_limits: 变化率限幅 (min, max)，不传则保持原值
        
        Example:
            # 只修改 w_cl，其他参数保持不变
            controller.set_config(w_cl=80.0)
            
            # 修改多个参数
            controller.set_config(w_cl=80.0, k_eso=3.0, output_limits=(-100, 100))
        """
        # 只更新传入的参数
        if order is not None:
            self.order = order
        if sample_time is not None:
            self.sample_time = sample_time
        if b0 is not None:
            self.b0 = b0
        if w_cl is not None:
            self.w_cl = w_cl
        if k_eso is not None:
            self.k_eso = k_eso
        
        # 对于可以为None的参数，使用...作为哨兵值
        if output_limits is not ...:
            self.output_limits = output_limits
        if rate_limits is not ...:
            self.rate_limits = rate_limits
        
        # 重新计算理论稳定时间
        if self.order == 1:
            self.settling_time = 4.0 / self.w_cl
        else:
            self.settling_time = 6.0 / self.w_cl
        
        # 重置控制器，应用新配置
        self.reset()

    def get_info(self) -> dict:
        """
        获取控制器信息
        
        Returns:
            dict: 包含控制器参数和性能指标
        """
        return {
            "type": "LADRC (Linear Active Disturbance Rejection Control)",
            "order": self.order,
            "sample_time": self.sample_time,
            "frequency": 1.0 / self.sample_time,
            "b0": self.b0,
            "w_cl": self.w_cl,
            "k_eso": self.k_eso,
            "observer_bandwidth": self.k_eso * self.w_cl,
            "settling_time": self.settling_time,
            "output_limits": self.output_limits,
            "rate_limits": self.rate_limits,
        }
    
    def print_info(self):
        """打印控制器信息"""
        info = self.get_info()
        print("=" * 60)
        print(f"🎛️  {info['type']}")
        print("=" * 60)
        print(f"阶数 (order):           {info['order']}")
        print(f"采样时间 (delta):       {info['sample_time']:.4f} 秒")
        print(f"控制频率:               {info['frequency']:.1f} Hz")
        print(f"系统增益 (b0):          {info['b0']}")
        print(f"闭环带宽 (w_cl):        {info['w_cl']:.1f} rad/s")
        print(f"观测器倍数 (k_eso):     {info['k_eso']}")
        print(f"观测器带宽:             {info['observer_bandwidth']:.1f} rad/s")
        print(f"理论稳定时间:           {info['settling_time']:.3f} 秒")
        print(f"输出限幅:               {info['output_limits']}")
        print(f"变化率限制:             {info['rate_limits']}")
        print("=" * 60)
    
    def __repr__(self) -> str:
        return (
            f"LADRCController(order={self.order}, "
            f"sample_time={self.sample_time}, "
            f"b0={self.b0}, "
            f"w_cl={self.w_cl}, "
            f"k_eso={self.k_eso})"
        )


# ============================================================================
# 预设配置
# ============================================================================

class LADRCPresets:
    """LADRC 控制器预设配置"""
    
    @staticmethod
    def fast_tracking(sample_time: float = 0.01) -> LADRCController:
        """
        快速跟踪配置
        适用场景：需要快速响应，目标变化快
        稳定时间: ~0.05秒
        """
        return LADRCController(
            order=1,
            sample_time=sample_time,
            b0=1.0,
            w_cl=80.0,
            k_eso=3.0
        )
    
    @staticmethod
    def balanced(sample_time: float = 0.01) -> LADRCController:
        """
        平衡配置（推荐）
        适用场景：大多数应用
        稳定时间: ~0.067秒
        """
        return LADRCController(
            order=1,
            sample_time=sample_time,
            b0=1.0,
            w_cl=60.0,
            k_eso=2.5
        )
    
    @staticmethod
    def stable(sample_time: float = 0.01) -> LADRCController:
        """
        稳定配置
        适用场景：需要平滑稳定，容忍稍慢响应
        稳定时间: ~0.1秒
        """
        return LADRCController(
            order=1,
            sample_time=sample_time,
            b0=1.0,
            w_cl=40.0,
            k_eso=2.0
        )
    
    @staticmethod
    def second_order(sample_time: float = 0.01) -> LADRCController:
        """
        二阶配置
        适用场景：需要控制位置和速度，更平滑的轨迹
        稳定时间: ~0.1秒
        """
        return LADRCController(
            order=2,
            sample_time=sample_time,
            b0=1.0,
            w_cl=60.0,
            k_eso=2.5
        )


# ============================================================================
# 调试指南 - 参数调整策略
# ============================================================================

"""
🔧 LADRC 参数调试指南

【问题 1】跟踪太慢，一直追不上目标
    症状：误差一直很大，响应迟钝
    解决：✅ 增大 w_cl (如 60 → 80 → 100)
         ❌ 不要增大 k_eso（这不会提高响应速度！）
    
【问题 2】震荡、不稳定、来回抖动
    症状：围绕目标震荡，无法稳定
    解决：✅ 减小 w_cl (如 60 → 50 → 40)
         ✅ 减小 k_eso (如 2.5 → 2.0)
    
【问题 3】误差能减小但消除得很慢
    症状：能跟上，但总有残余误差
    解决：✅ 减小 b0 (如 1.0 → 0.8 → 0.6)
         说明系统增益估计偏大
    
【问题 4】对扰动反应慢（如突然的外力）
    症状：基本跟踪正常，但遇到扰动反应慢
    解决：✅ 增大 k_eso (如 2.5 → 3.0)
    
【问题 5】输出经常达到限幅
    症状：控制输出总是达到 ±4000 上限
    解决：✅ 增大 output_limits
         或 ✅ 减小 w_cl（降低需求）
         或 ✅ 增大 b0（控制器认为系统增益太小）

推荐调试顺序：
1. 先调 w_cl，找到合适的响应速度
2. 再调 b0，确保误差能消除
3. 最后微调 k_eso，优化抗扰性能
4. k_eso 通常保持 2.0-3.0 即可
"""


# ============================================================================
# 使用示例
# ============================================================================

if __name__ == "__main__":
    import time
    import math
    
    print("\n" + "=" * 70)
    print("LADRC 控制器示例")
    print("=" * 70 + "\n")
    
    # 1. 创建控制器
    controller = LADRCPresets.balanced(sample_time=0.01)
    controller.print_info()
    
    # 2. 模拟跟踪控制
    print("\n🎯 模拟跟踪正弦目标...\n")
    
    dt = 0.01  # 10ms 控制周期
    current_position = 0.0
    
    for i in range(200):
        t = i * dt
        
        # 目标：正弦波
        target = 100 * math.sin(2 * math.pi * 0.5 * t)
        
        # 计算误差
        error = target - current_position
        
        # LADRC 控制
        output = controller.compute(error)
        
        # 应用控制输出
        current_position += output * dt
        
        # 每 0.5 秒打印一次
        if i % 50 == 0:
            print(f"t={t:.2f}s | 目标={target:7.2f} | "
                  f"当前={current_position:7.2f} | 误差={error:6.2f}")
        
        time.sleep(dt)
    
    print("\n✅ 示例完成！")

