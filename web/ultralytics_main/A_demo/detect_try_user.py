import cv2
from ultralytics import YOLO

def detect_try_(input_path, confidence_threshold, output_path):
    # 1. 加载 YOLO 模型
    model = YOLO("D:/python_all/tracer-53e05801b2f2e12436b14246a1d0ebda604cd921/web/ultralytics_main/A_demo/yolov8n.pt")

    # 2. 检测输入是图像还是视频
    if input_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
        # 处理图像
        image = cv2.imread(input_path)
        results = model(image)  # 对图片进行预测

        # 在图像上绘制边界框和标签
        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = float(box.conf[0])
                class_id = int(box.cls[0])

                if confidence >= confidence_threshold:
                    cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
                    label = f'{class_id}, {confidence:.2f}'
                    cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # 保存处理后的图像
        cv2.imwrite(output_path, image)

    elif input_path.lower().endswith(('.mp4', '.avi', '.mov')):
        # 处理视频
        cap = cv2.VideoCapture(input_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            results = model(frame)

            for result in results:
                boxes = result.boxes
                for box in boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    confidence = float(box.conf[0])
                    class_id = int(box.cls[0])

                    if confidence >= confidence_threshold:
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                        label = f'{class_id}, {confidence:.2f}'
                        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

            out.write(frame)

        cap.release()
        out.release()

    else:
        raise ValueError("Unsupported file format. Please provide an image or video file.")

# 示例调用


if __name__ == '__main__':
    image = detect_try_(r'D:\python_all\tracer-53e05801b2f2e12436b14246a1d0ebda604cd921\media\19546051318\1 (2).jpg',
                        0.5,
                        r'D:\python_all\tracer-53e05801b2f2e12436b14246a1d0ebda604cd921\media\19546051318\1 (2)_try_train.jpg',
                        )
