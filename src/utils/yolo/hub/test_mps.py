from ultralytics import YOLO, checks, hub

if __name__ == '__main__':
    # Windows 多进程保护，必须添加！
    checks()
    
    hub.login('8ab9fcaa370320553b9aa35f28a0986c1fbd4fa0b3')
    
    model = YOLO('https://hub.ultralytics.com/models/nYLMvGSKN7PuNcVTnbC8')
    results = model.train()