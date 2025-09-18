from threading import Lock
from data_center.index_type import State, User, Order


class DataCenter:
    """数据中心单例，管理全局状态"""
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
        if not self._initialized:
            self.state = State()
            self._initialized = True
    
    def get_state(self) -> State:
        """获取当前状态"""
        return self.state
    
    def set_state(self, state: State):
        """设置新状态"""
        with self._lock:
            self.state = state
    
    def reset_state(self):
        """重置状态到初始值"""
        with self._lock:
            self.state = State()


# 创建全局单例实例
data_center = DataCenter()

# 获取数据中心实例的便捷函数
def get_data_center() -> DataCenter:
    """获取全局数据中心单例实例"""
    return data_center


# 示例使用（可以删除）
if __name__ == "__main__":
    dc = DataCenter()
    dc.state.user.name = "Alice"
    dc.state.user.age = 30
    dc.state.order.name = "Laptop"
    dc.state.order.price = 1200
    dc.state.yolo_model_state.model_path = "yolo_model.pt"
    # 全局任何地方获取
    dc2 = DataCenter()
    print("用户信息:", dc2.state.user)
    print("订单信息:", dc2.state.order)
    print("YOLO模型信息:", dc2.state.yolo_model_state)
