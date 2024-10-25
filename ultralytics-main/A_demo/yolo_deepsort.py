import cv2
import torch
from deep_sort import DeepSort  # 确保你已正确安装 Deep SORT

# 初始化 YOLOv5 模型
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# 初始化 Deep SORT
deep_sort = DeepSort()

# 打开视频文件或摄像头
cap = cv2.VideoCapture(0)  # 或使用 0 访问摄像头

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 使用 YOLO 进行目标检测
    results = model(frame)
    detections = results.xyxy[0].cpu().numpy()  # 获取检测结果

    # 处理检测结果
    bbox = detections[:, :4]  # [x1, y1, x2, y2]
    scores = detections[:, 4]  # 置信度
    classes = detections[:, 5]  # 类别

    # 过滤低置信度的检测
    confidence_threshold = 0.3
    valid_detections = [(x1, y1, x2, y2, score) for (x1, y1, x2, y2, score) in detections if score > confidence_threshold]

    # 使用 Deep SORT 进行跟踪
    tracked_objects = deep_sort.update(valid_detections, frame)

    # 绘制边界框和跟踪 ID
    for obj in tracked_objects:
        x1, y1, x2, y2, obj_id = obj[:5]  # Deep SORT 输出的格式
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)
        cv2.putText(frame, f'ID: {int(obj_id)}', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    cv2.imshow('YOLO + Deep SORT Object Tracking', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()