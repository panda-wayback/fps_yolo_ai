import torch
print(torch.__version__)
torch.backends.mps.is_available()  # True 表示可以用 MPS 加速
print(torch.backends.mps.is_available())
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
print(device)
