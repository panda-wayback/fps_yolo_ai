from data_center.models.base_state import BaseState, ReactiveVar


class ControllerModel(BaseState):
    """
    PID模型状态类，管理PID相关参数和状态
    """
    order: ReactiveVar[int] = 1  # 控制器阶数
    sample_time: ReactiveVar[float] = 0.01  # 采样时间
    b0: ReactiveVar[float] = 1.0  # 控制增益
    w_cl: ReactiveVar[float] = 60.0  # 控制器带宽
    k_eso: ReactiveVar[float] = 2.5  # ESO增益
    output_limits: ReactiveVar[tuple[float, float]] = None  # 输出限幅
    rate_limits: ReactiveVar[tuple[float, float]] = None  # 变化率限幅

    output: ReactiveVar[tuple[float, float]] = None  # 输出
    error: ReactiveVar[tuple[float, float]] = None  # 误差
