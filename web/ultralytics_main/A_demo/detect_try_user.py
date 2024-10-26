import cv2
import os
from ultralytics import YOLO


def detect_try_(user_image_path, confidence_threshold, save_path):
    # 1. 加载 YOLO 模型
    model = YOLO(
        "D:/python_all/tracer-53e05801b2f2e12436b14246a1d0ebda604cd921/web/ultralytics_main/A_demo/yolov8n.pt")  # 加载官方 YOLOv8 模型

    # 2. 指定图片路径
    image_path = user_image_path

    # 3. 使用模型进行预测
    results = model(image_path)  # 对图片进行预测

    # 4. 读取图像
    image = cv2.imread(image_path)  # 读取图片

    # 在图像上绘制边界框和标签
    for result in results:
        boxes = result.boxes  # 获取边界框
        for box in boxes:
            # 获取边界框坐标
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # 获取坐标并转换为整数
            confidence = float(box.conf[0])  # 获取置信度分数
            class_id = int(box.cls[0])  # 获取类别 ID

            # 仅在置信度高于阈值时绘制
            if confidence >= confidence_threshold:
                # 在图像上绘制边界框
                cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)  # 绘制矩形框

                # 准备标签和置信度
                label = f'{class_id}, {confidence:.2f}'

                # 在图像上绘制标签
                # cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # 5. 保存处理后的图像到指定路径
    cv2.imwrite(save_path, image)  # 保存图像

def get_unique_file_name(directory, file_name, file_extension):
    # 初始文件名
    new_file_name = f"{file_name}_try{file_extension}"
    new_file_path = os.path.join(directory, new_file_name)

    # 检查文件名是否已经存在，如果存在则递增数字
    counter = 1
    while os.path.exists(new_file_path):
        new_file_name = f"{file_name}_try_{counter}{file_extension}"
        new_file_path = os.path.join(directory, new_file_name)
        counter += 1

    return new_file_name, new_file_path

#
# if __name__ == '__main__':
#     image = detect_try_(r'D:\python_all\tracer-53e05801b2f2e12436b14246a1d0ebda604cd921\media\19546051318\1 (2).jpg',
#                         0.5,
#                         r'D:\python_all\tracer-53e05801b2f2e12436b14246a1d0ebda604cd921\media\19546051318\1 (2)_try_train.jpg',
#                         )
