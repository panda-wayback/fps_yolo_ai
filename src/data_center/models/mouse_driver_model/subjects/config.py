"""
鼠标驱动配置话题处理
基于PID模型的最佳实践
"""

import time
from data_center.index import get_data_center
from data_center.models.mouse_driver_model.state_model import MouseDriverState
from data_center.models.mouse_driver_model.subject_model import MouseDriverSubjectModel
from singleton_classes.simulation_move_mouse.simulation_move_mouse import get_mouse_simulator


def submit_config(config: MouseDriverState):
    """执行鼠标模拟器配置"""
    try:
        get_mouse_simulator().run()
        print(f"✅ 鼠标模拟器已启动，配置: fps={config.fps}, smoothing={config.smoothing}")
    except Exception as e:
        print(f"❌ 鼠标模拟器启动失败: {e}")


def update_mouse_driver_state(config: MouseDriverState):
    """更新鼠标驱动状态"""
    try:
        state = get_data_center().state.mouse_driver_state
        state.merge_state(config)
        print(f"✅ 鼠标驱动状态已更新: fps={config.fps}, smoothing={config.smoothing}, running={config.running}")
    except Exception as e:
        print(f"❌ 鼠标驱动状态更新失败: {e}")


def init_config_subject():
    """初始化鼠标驱动配置订阅"""
    MouseDriverSubjectModel.config_subject.subscribe(submit_config)
    MouseDriverSubjectModel.config_subject.subscribe(update_mouse_driver_state)


init_config_subject()


if __name__ == "__main__":
    # 测试用例
    config = MouseDriverState(
        fps=1000, 
        smoothing=0.4, 
        max_duration=0.05, 
        decay_rate=0.95, 
        running=True
    )
    MouseDriverSubjectModel.config_subject.on_next(config)
    time.sleep(1)