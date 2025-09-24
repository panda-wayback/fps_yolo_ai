from ultralytics import YOLO, checks, hub
checks()

hub.login('8ab9fcaa370320553b9aa35f28a0986c1fbd4fa0b3')

model = YOLO('https://hub.ultralytics.com/models/KZKrqH902vHee2vFTCTZ')
results = model.train()