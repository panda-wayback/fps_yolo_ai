"""
测试State类的JSON序列化功能
"""

import numpy as np
from data_state import State


def test_json_serialization():
    """测试JSON序列化和反序列化"""
    print("=== 测试State JSON序列化 ===")
    
    # 创建一个State实例
    state = State()
    state.a_threshold = 15
    state.b_suffix = "!!!"
    state.a_value = 5
    state.b_text = "world"
    state.mouse_pos = (300, 200)
    state.region = (400, 300)
    
    # 添加一个测试图像
    test_image = np.random.randint(0, 255, (100, 150, 3), dtype=np.uint8)
    state.screenshot_img = test_image
    
    print("原始State:")
    print(f"  a_threshold: {state.a_threshold}")
    print(f"  b_suffix: {state.b_suffix}")
    print(f"  a_value: {state.a_value}")
    print(f"  b_text: {state.b_text}")
    print(f"  mouse_pos: {state.mouse_pos}")
    print(f"  region: {state.region}")
    print(f"  screenshot_img shape: {state.screenshot_img.shape}")
    
    # 转换为字典
    print("\n转换为字典:")
    state_dict = state.to_dict()
    print(f"字典键: {list(state_dict.keys())}")
    print(f"screenshot_img类型: {type(state_dict['screenshot_img'])}")
    
    # 转换为JSON
    print("\n转换为JSON:")
    json_str = state.to_json()
    print(f"JSON长度: {len(json_str)} 字符")
    print("JSON内容预览:")
    print(json_str[:200] + "..." if len(json_str) > 200 else json_str)
    
    # 从JSON恢复
    print("\n从JSON恢复:")
    restored_state = State.from_json(json_str)
    print(f"  a_threshold: {restored_state.a_threshold}")
    print(f"  b_suffix: {restored_state.b_suffix}")
    print(f"  a_value: {restored_state.a_value}")
    print(f"  b_text: {restored_state.b_text}")
    print(f"  mouse_pos: {restored_state.mouse_pos}")
    print(f"  region: {restored_state.region}")
    print(f"  screenshot_img shape: {restored_state.screenshot_img.shape}")
    
    # 验证图像数据是否一致
    if np.array_equal(state.screenshot_img, restored_state.screenshot_img):
        print("✅ 图像数据完全一致")
    else:
        print("❌ 图像数据不一致")
    
    # 验证其他数据是否一致
    if (state.a_threshold == restored_state.a_threshold and
        state.b_suffix == restored_state.b_suffix and
        state.a_value == restored_state.a_value and
        state.b_text == restored_state.b_text and
        state.mouse_pos == restored_state.mouse_pos and
        state.region == restored_state.region):
        print("✅ 所有数据完全一致")
    else:
        print("❌ 数据不一致")


def test_without_image():
    """测试没有图像时的序列化"""
    print("\n=== 测试无图像序列化 ===")
    
    state = State()
    state.a_threshold = 20
    state.b_suffix = "???"
    state.mouse_pos = (500, 400)
    state.region = (600, 500)
    # screenshot_img 保持为 None
    
    print("原始State (无图像):")
    print(f"  screenshot_img: {state.screenshot_img}")
    
    # 转换为JSON
    json_str = state.to_json()
    print(f"\nJSON内容:")
    print(json_str)
    
    # 从JSON恢复
    restored_state = State.from_json(json_str)
    print(f"\n恢复后State:")
    print(f"  screenshot_img: {restored_state.screenshot_img}")
    
    if restored_state.screenshot_img is None:
        print("✅ 图像字段正确保持为None")
    else:
        print("❌ 图像字段应该为None")


def test_save_load_file():
    """测试保存到文件和从文件加载"""
    print("\n=== 测试文件保存和加载 ===")
    
    # 创建State
    state = State()
    state.a_threshold = 25
    state.b_suffix = "###"
    state.mouse_pos = (800, 600)
    state.region = (1000, 800)
    state.screenshot_img = np.zeros((50, 50, 3), dtype=np.uint8)
    
    # 保存到文件
    filename = "test_state.json"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(state.to_json())
    print(f"✅ 已保存到文件: {filename}")
    
    # 从文件加载
    with open(filename, 'r', encoding='utf-8') as f:
        loaded_json = f.read()
    
    loaded_state = State.from_json(loaded_json)
    print(f"✅ 已从文件加载")
    print(f"  a_threshold: {loaded_state.a_threshold}")
    print(f"  mouse_pos: {loaded_state.mouse_pos}")
    print(f"  region: {loaded_state.region}")
    print(f"  screenshot_img shape: {loaded_state.screenshot_img.shape}")


if __name__ == "__main__":
    test_json_serialization()
    test_without_image()
    test_save_load_file()
    print("\n🎉 所有测试完成！")
