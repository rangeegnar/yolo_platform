import os
import django

# 设置设置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tracer.settings')

# 初始化 Django
django.setup()

# 在初始化后导入模型
from web import models


def run(pretrain_list):
    # 检查数据库中是否已有预训练模型
    exists = models.Pretrain_model.objects.first()

    # 如果数据库中没有预训练模型，则添加列表中的模型
    if not exists:
        for pretrain in pretrain_list:
            models.Pretrain_model.objects.create(
                name=pretrain  # 将模型名称存入数据库
            )


if __name__ == '__main__':
    pretrain_list = [
        'yolo11l.pt',
        'yolo11m.pt',
        'yolo11n.pt',
        'yolo11s.pt',
        'yolov10l.pt',
        'yolov10m.pt',
        'yolov10n.pt',
        'yolov10s.pt',
        'yolov8l.pt',
        'yolov8m.pt',
        'yolov8n.pt',
        'yolov8s.pt',
    ]

    # 运行函数以添加预训练模型到数据库
    run(pretrain_list)