#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 pyautogui 是否能触发 GetAsyncKeyState 监听
"""
import ctypes
import time
import pyautogui

# Windows 虚拟键码
VK_LBUTTON = 0x01  # 左键

def check_key_state(vk_code):
    """检查按键状态"""
    state = ctypes.windll.user32.GetAsyncKeyState(vk_code)
    return state & 0x8000 != 0

def test_pyautogui_detection():
    """测试 pyautogui 点击是否能被检测到"""
    print("=" * 60)
    print("测试: pyautogui 点击是否能触发 GetAsyncKeyState 监听")
    print("=" * 60)
    
    print("\n准备在 2 秒后执行 pyautogui 点击...")
    time.sleep(2)
    
    print("开始监听...")
    start_time = time.time()
    detected = False
    
    # 在后台线程中执行点击（按住更久）
    import threading
    def click_after_delay():
        time.sleep(0.5)
        print("\n>>> pyautogui.mouseDown() - 按下左键")
        pyautogui.mouseDown()
        time.sleep(0.1)  # 按住 0.5 秒
        print(">>> pyautogui.mouseUp() - 释放左键")
        pyautogui.mouseUp()
    
    thread = threading.Thread(target=click_after_delay)
    thread.start()
    
    # 监听 2 秒
    while time.time() - start_time < 2:
        is_pressed = check_key_state(VK_LBUTTON)
        
        if is_pressed and not detected:
            detected = True
            print(f"\n✅ 检测到鼠标左键按下！(用时 {time.time() - start_time:.3f}s)")
            print("   说明：GetAsyncKeyState 可以检测到 pyautogui 的点击")
        
        time.sleep(0.01)  # 10ms 轮询
    
    thread.join()
    
    print("\n" + "=" * 60)
    if detected:
        print("结果: ✅ pyautogui 可以触发 GetAsyncKeyState 监听")
    else:
        print("结果: ❌ pyautogui 不能触发 GetAsyncKeyState 监听")
        print("      （或者点击太快没被检测到）")
    print("=" * 60)


def test_direct_click():
    """测试物理点击（作为对照）"""
    print("\n\n" + "=" * 60)
    print("对照测试: 请手动点击鼠标左键")
    print("=" * 60)
    print("监听中... (按 Ctrl+C 退出)")
    
    try:
        last_state = False
        while True:
            is_pressed = check_key_state(VK_LBUTTON)
            
            if is_pressed != last_state:
                if is_pressed:
                    print("✅ 检测到鼠标左键按下")
                else:
                    print("✅ 检测到鼠标左键释放")
                last_state = is_pressed
            
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("\n监听已停止")


if __name__ == "__main__":
    # 测试1: pyautogui 模拟点击
    test_pyautogui_detection()
    
    # 测试2: 物理点击（可选）
    response = input("\n是否测试物理点击? (y/n): ")
    if response.lower() == 'y':
        test_direct_click()

