from data_center.models.base_state import BaseState, ReactiveVar


class ControllerModel(BaseState):
    """
    ADRC控制器模型状态类，管理ADRC相关参数和状态
    """
    # ADRC控制器参数
    order: ReactiveVar[int] = 1  # 控制器阶数 (1或2)
    sample_time: ReactiveVar[float] = 0.01  # 采样时间（秒）
    b0: ReactiveVar[float] = 1.0  # 控制增益
    w_cl: ReactiveVar[float] = 60.0  # 控制器带宽
    k_eso: ReactiveVar[float] = 2.5  # ESO（扩张状态观测器）增益
    output_limits: ReactiveVar[tuple[float, float]] = None  # 输出限幅 (min, max)
    rate_limits: ReactiveVar[tuple[float, float]] = None  # 变化率限幅 (min, max)

    # 运行状态
    output: ReactiveVar[tuple[float, float]] = None  # 控制器输出 (x, y)
    error: ReactiveVar[tuple[float, float]] = None  # 误差值 (x, y)
    is_enabled: ReactiveVar[bool] = False  # 控制器是否启用
