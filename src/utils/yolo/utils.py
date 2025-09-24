import torch


def get_device() -> str:
    """获取最佳计算设备"""
    if torch.backends.mps.is_available():
        return 'mps'
    elif torch.cuda.is_available():
        return 'cuda'
    else:
        return 'cpu'