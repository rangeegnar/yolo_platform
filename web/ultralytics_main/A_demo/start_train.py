import time
import warnings
from ultralytics import YOLO

warnings.filterwarnings("ignore")



# 加载模型
model = YOLO("../ultralytics/cfg/models/v8/yolov8.yaml").load("yolov8n.pt")

# 训练模型
results = model.train(
    data='D:/python_all/tracer-53e05801b2f2e12436b14246a1d0ebda604cd921/web/ultralytics_main/data.yaml',
    epochs=10,
    imgsz=640,
    device='cpu',
    workers=0,
    batch=4,
    cache=True
)

# 等待10秒
time.sleep(10)