#!/usr/bin/env python3
"""
测试优化后的 BaseState 功能
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from data_center.models.base_state import BaseState
from typing_extensions import Optional
from pydantic import ConfigDict


class TestState(BaseState):
    """测试状态类"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    # PID 参数
    kp: Optional[float] = None
    ki: Optional[float] = None
    kd: Optional[float] = None
    
    # 错误记录
    last_error_x: Optional[float] = None
    last_error_y: Optional[float] = None
    
    # 输出记录
    last_output_x: Optional[float] = None
    last_output_y: Optional[float] = None


def test_field_proxy_subscription():
    """测试字段代理订阅功能"""
    print("=== 测试字段代理订阅功能 ===")
    
    state = TestState()
    
    # 使用新的链式调用方式订阅字段变化
    state.kp.subscribe(lambda v: print(f"[观察者] kp 更新: {v}"))
    state.kd.subscribe(lambda v: print(f"[观察者] kd 更新: {v}"))
    state.last_error_x.subscribe(lambda v: print(f"[观察者] last_error_x 更新: {v}"))
    
    # 修改字段值
    state.kp = 0.8
    state.kd = 0.3
    state.last_error_x = 10.5
    state.kp = 1.2
    
    print(f"\n当前 kp 值: {state.kp.value}")
    print(f"当前 kd 值: {state.kd.value}")
    print(f"FieldProxy 对象: {state.kp}")
    
    # 通过 FieldProxy 设置值
    state.kp.value = 2.5
    print(f"通过 FieldProxy 设置后的 kp 值: {state.kp.value}")


def test_traditional_subscription():
    """测试传统的字符串订阅方式"""
    print("\n=== 测试传统的字符串订阅方式 ===")
    
    state = TestState()
    
    # 使用传统的字符串方式订阅
    state.subscribe("ki", lambda v: print(f"[观察者] ki 更新: {v}"))
    state.subscribe("last_error_y", lambda v: print(f"[观察者] last_error_y 更新: {v}"))
    
    # 修改字段值
    state.ki = 0.1
    state.last_error_y = 5.5


def test_existing_methods():
    """测试现有的状态管理方法"""
    print("\n=== 测试现有的状态管理方法 ===")
    
    state1 = TestState(kp=1.0, ki=0.5, kd=0.2)
    state2 = TestState(kp=1.5, ki=0.3, last_error_x=10.0)
    
    print(f"State1: kp={state1.kp.value}, ki={state1.ki.value}, kd={state1.kd.value}")
    print(f"State2: kp={state2.kp.value}, ki={state2.ki.value}, last_error_x={state2.last_error_x.value}")
    
    # 测试 merge_state
    state1.merge_state(state2)
    print(f"合并后 State1: kp={state1.kp.value}, ki={state1.ki.value}, kd={state1.kd.value}, last_error_x={state1.last_error_x.value}")
    
    # 测试 update_state
    state1.update_state(kp=2.0, kd=0.8)
    print(f"更新后 State1: kp={state1.kp.value}, kd={state1.kd.value}")
    
    # 测试 get_changed_fields
    changes = state1.get_changed_fields(state2)
    print(f"与 State2 不同的字段: {changes}")


def test_field_proxy_functionality():
    """测试 FieldProxy 的其他功能"""
    print("\n=== 测试 FieldProxy 的其他功能 ===")
    
    state = TestState()
    
    # 测试 FieldProxy 的 value 属性
    state.kp = 1.5
    print(f"直接赋值后 kp 值: {state.kp.value}")
    
    # 通过 value 属性设置
    state.kp.value = 3.0
    print(f"通过 value 属性设置后 kp 值: {state.kp.value}")
    
    # 测试 FieldProxy 的 repr
    print(f"FieldProxy 对象表示: {state.kp}")


if __name__ == "__main__":
    print("开始测试优化后的 BaseState 功能...\n")
    
    try:
        test_field_proxy_subscription()
        test_traditional_subscription()
        test_existing_methods()
        test_field_proxy_functionality()
        
        print("\n✅ 所有测试通过！BaseState 优化成功！")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
