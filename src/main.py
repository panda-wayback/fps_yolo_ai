"""
FPS游戏AI辅助主程序 - 最小示例
加载YOLO模型并检测鼠标周围的目标，显示截图和检测结果
"""

import time
import cv2
from pynput import keyboard

from functions.get_pid_res import get_pid_res
from functions.get_target_vector import get_center_to_target_vector
from functions.ims_show import show_image
from functions.run_move_mouse import run_move_mouse_by_pid

from fps_models.aimlabs import get_aimlabs_model
from functions.get_sight_images import get_mouse_region_image
from singleton_classes.data_center import DataCenter
from singleton_classes.screenshot_img.main import MouseScreenshot



def print_detection_info(results, image_size = (400, 300)):
    # 处理检测结果
    res = results[0]  # 单张图像
    boxes = res.boxes.xyxy  # 边界框 (x1, y1, x2, y2)
    classes = res.boxes.cls  # 类别索引
    confidences = res.boxes.conf  # 置信度

    if len(boxes) > 0:
        print(f"检测到 {len(boxes)} 个目标:")
        print(f"目标中心点: {get_center_to_target_vector(res, image_size)}")
        print(f"PID控制器输出: {get_pid_res(res, image_size)}")
        # for i, box in enumerate(boxes):
        #     x1, y1, x2, y2 = box.tolist()
        #     cls = int(classes[i])
        #     conf = float(confidences[i])
        #     # print(f"  目标 {i+1}: 类别 {cls}, 置信度 {conf:.2f}, 位置 [{x1:.0f}, {y1:.0f}, {x2:.0f}, {y2:.0f}]")
    else:
        print("未检测到目标")

# 自动瞄准
def auto_aim(results, image_size = (400, 300)):
    """自动瞄准功能"""
    res = results[0]  # 单张图像
    run_move_mouse_by_pid(res, image_size)


def main():
    """主函数 - 显示截图和检测结果"""
    print("=== FPS AI辅助系统 - 实时检测显示 ===")
    print("控制说明:")
    print("  'q' 键或 'ESC' 键 - 退出程序")
    print("  'SPACE' 键 - 暂停/继续程序")
    print("  '1' 键 - 开启自动瞄准")
    print("  '2' 键 - 关闭自动瞄准")
    
    # 全局控制变量
    global running, paused, auto_aim_enabled
    running = True
    paused = False
    auto_aim_enabled = False  # 自动瞄准开关
    
    def on_key_press(key):
        """键盘按键处理函数"""
        global running, paused, auto_aim_enabled
        try:
            # 检查退出键
            if key == keyboard.Key.esc or (hasattr(key, 'char') and key.char == 'q'):
                print("\n🛑 检测到退出信号，正在安全退出...")
                running = False
                return False  # 停止监听器
            
            # 检查暂停键
            elif key == keyboard.Key.space:
                paused = not paused
                status = "暂停" if paused else "继续"
                print(f"\n⏸️  程序已{status}")
            
            # 检查自动瞄准控制键
            elif hasattr(key, 'char'):
                if key.char == '1':
                    auto_aim_enabled = True
                    print("\n🎯 自动瞄准已开启")
                elif key.char == '2':
                    auto_aim_enabled = False
                    print("\n🚫 自动瞄准已关闭")
                
        except AttributeError:
            # 特殊键（如ESC）没有char属性
            pass
    
    # 启动键盘监听器
    listener = keyboard.Listener(on_press=on_key_press)
    listener.start()
    
    # 加载模型
    model = get_aimlabs_model()
    if model is None:
        print("❌ 模型加载失败，程序退出")
        listener.stop()
        return
    

    
    print("✅ 程序已启动，开始实时检测...")
    print("💡 提示: 按 '1' 键开启自动瞄准功能")
    
    # 设置截图区域大小
    width, height = 600, 400
    # 获取鼠标位置（只获取一次，提高性能）
    mouse_x, mouse_y = (756, 509)
    
    MouseScreenshot().start((mouse_x, mouse_y), (width, height), 0.02)
    
    try:
        while running:
            # 如果程序暂停，跳过本次循环
            if paused:
                time.sleep(0.1)  # 暂停时降低CPU使用率
                continue
            

            
            # 获取鼠标周围图像（传入鼠标位置避免重复获取）
            image = DataCenter().get_state().screenshot_img
            # image = get_mouse_region_image(width, height, (mouse_x, mouse_y))
            # 进行目标检测
            results = model(image, verbose=False)
            
            # 显示图像
            show_image(image, results)

            # 根据按键状态决定是否执行自动瞄准
            if auto_aim_enabled:
                auto_aim(results, (width, height))
            
            # 控制帧率 (约1000fps，但实际受检测速度限制)
            time.sleep(0.001)
            
            # 非阻塞的OpenCV按键检查（作为备用）
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    except KeyboardInterrupt:
        print("\n🛑 检测到Ctrl+C，正在安全退出...")
    except Exception as e:
        print(f"\n❌ 程序运行出错: {e}")
    finally:
        # 清理资源
        running = False
        listener.stop()
        cv2.destroyAllWindows()
        print("✅ 程序已安全退出")



if __name__ == "__main__":
    main()
