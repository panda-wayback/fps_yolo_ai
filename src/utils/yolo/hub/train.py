import torch
from ultralytics import YOLO, checks, hub

# 检查系统环境
checks()

# 检查MPS是否可用
if torch.backends.mps.is_available():
    device = 'mps'
    print("✅ 检测到MPS支持，将使用GPU加速")
elif torch.cuda.is_available():
    device = 'cuda'
    print("✅ 检测到CUDA支持，将使用GPU加速")
else:
    device = 'cpu'
    print("⚠️  未检测到GPU支持，将使用CPU训练")

print(f"使用设备: {device}")

hub.login('8ab9fcaa370320553b9aa35f28a0986c1fbd4fa0b3')

model = YOLO('https://hub.ultralytics.com/models/YHJSUcWMlckhq3dbmwoY')

# 将模型移动到指定设备
model.to(device)
results = model.train()

print("训练完成！")