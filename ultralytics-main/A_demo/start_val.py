import time
from ultralytics import YOLO

model = YOLO('yolov8.pt')  # 使用自己的best哈!
results = model.train(data='my_data.yaml', epochs=100, imgsz=640, device='cpu', workers=0, batch=4,
                      cache=True)  # 开始训练
time.sleep(10)  # 睡眠10s，主要是用于服务器多次训练的过程中使用