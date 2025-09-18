from pydantic import BaseModel, ConfigDict
from typing import Any, Dict


class BaseState(BaseModel):
    """状态管理基类，提供通用的更新方法"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    def update_state(self, **kwargs):
        """更新状态，只更新提供的字段，保持其他字段不变"""
        for key, value in kwargs.items():
            if key in self.model_fields:
                setattr(self, key, value)
    
    def merge_state(self, other_state: 'BaseState'):
        """合并另一个状态对象，other_state的字段优先"""
        if other_state is not None:
            # 只合并非None的字段
            update_data = {}
            for key, value in other_state.model_dump().items():
                if value is not None:
                    update_data[key] = value
            self.update_state(**update_data)
    
    def reset_to_defaults(self):
        """重置所有字段为默认值"""
        for field_name, field_info in self.model_fields.items():
            setattr(self, field_name, field_info.default)
    
    def get_changed_fields(self, other_state: 'BaseState') -> Dict[str, Any]:
        """获取与另一个状态对象不同的字段"""
        if other_state is None:
            return {}
        
        changed = {}
        for key in self.model_fields:
            current_value = getattr(self, key)
            other_value = getattr(other_state, key)
            if current_value != other_value:
                changed[key] = current_value
        return changed
